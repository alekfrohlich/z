"""This module provides a class to draw objects given a Cairo.Context and the
viewport's resolution.

Classes
-------
    ObjectPainter

"""
import numpy as np
from scipy import special

from .models.curve import Interpolator
from util.clipping import clip_line


def init_forward_differences(shifts: 'list') -> 'list':
    """Initialize the first n forward differences where n is the number of
    shifts provided as input.

    Notes
    -----
        The initial forward differences are calculated using the reccurence
        relation:

            D^(k)[fn] = sum from t=0 to k of binom(k,t)*(-1)^t*fn+k-t

    References
    --------
        https://en.wikipedia.org/wiki/Recurrence_relation

    """
    fwd = [shifts[0]]
    for i in range(1, len(shifts)):
        temp = 0
        for j in range(i + 1):
            temp += special.binom(i, j) * (-1)**j * shifts[i-j]
        fwd.append(temp)
    return fwd


class ObjectPainter:
    """"""
    def __init__(self, cr: 'Cairo.Context', resolution: 'tuple'):
        self._cr = cr
        self._res = resolution

    def resolution_transform(self, point: 'tuple') -> 'tuple':
        """Rescale points from normalized coordinate system to resolution.

        Notes
        -----
            10 is added to both transformed coordinates to account for
            the clip region.

        """
        x_w, y_w = point
        x_vp = (x_w + 1) / (2) * self._res[0] + 10
        y_vp = (1 - (y_w + 1) / (2)) * self._res[1] + 10
        return (x_vp, y_vp)

    def paint_point(self, point: 'Point'):
        """Draw point."""
        p = self.resolution_transform(point.cached_points[0])
        self._cr.move_to(*p)
        self._cr.line_to(*p)
        self._cr.stroke()

    def paint_line(self, line: 'Line'):
        """Draw line."""
        p0, p1 = list(map(self.resolution_transform, line.cached_points))
        self._cr.move_to(*p0)
        self._cr.line_to(*p1)
        self._cr.stroke()

    def paint_polymesh(self, mesh: 'Mesh'):
        """Draw vertex-face mesh."""
        points = list(map(self.resolution_transform, mesh.cached_points))
        for face in mesh.cached_faces:
            self._cr.move_to(*points[face[0]])
            for i in face[1:]:
                self._cr.line_to(*points[i])
            self._cr.line_to(*points[face[0]])
            self._cr.stroke()

    def paint_curve(self, curve: 'Curve'):
        """Draw curve."""
        cp = curve.cached_points
        if curve.bmat is Interpolator.BEZIER:
            self._generate_segment(100, curve.bmat, cp[:4])
            for i in range((len(cp) - 4) // 2):
                geometry = [cp[2*i+3], cp[2*i+2],
                            cp[2*i+4], cp[2*i+5]]
                self._generate_segment(100, curve.bmat, geometry)
        else:
            for i in range(len(cp) - 3):
                self._generate_segment(100, curve.bmat, cp[i:i+4])

    def paint_surface(self, surface: 'Surface'):
        """Draw bicubic bezier surface."""
        def setup(curves: 'list', u: 'bool') -> 'tuple':
            """Initialize algorithm for drawing the family of curves in u or v."""
            interpolator = surface.bmatu if u else surface.bmatv
            dim = dimu if u else dimv
            fwd_x = []; fwd_y = []; prev_out = [True] * dim; prev_point = [None] * dim
            for i in range(dim):
                fx, fy = self._init_curve_algorithm(interpolator, curves[i], delta)
                fwd_x.append(fx)
                fwd_y.append(fy)

            return (fwd_x, fwd_y, prev_out, prev_point)

        def draw(u: 'bool'):
            """Draw family of curves."""
            interpolator = surface.bmatu if u else surface.bmatv
            dim1 = dimu if u else dimv; dim2 = dimv if u else dimu
            for _ in range(n+1):
                self._generate_segment(n, interpolator, [(fwd_x[i][0], fwd_y[i][0]) for i in range(dim1)])
                for i in range(dim2):
                    for j in range(dim2 - 1):
                        fwd_x[i][j] += fwd_x[i][j+1]
                        fwd_y[i][j] += fwd_y[i][j+1]
            self._cr.stroke()

        n = 20
        delta = 1 / n
        dimu = surface.bmatu.shape[0]
        dimv = surface.bmatv.shape[0]

        cp = surface.cached_points
        curves_in_u = [cp[dimu*i : dimu*i + dimu] for i in range(dimu)]
        curves_in_v = [[cp[i], cp[dimv+i], cp[2*dimv+i], cp[3*dimv+i]] for i in range(dimv)]

        U = True; V = False
        fwd_x, fwd_y, prev_out, prev_point = setup(curves_in_u, U)
        draw(U)
        fwd_x, fwd_y, prev_out, prev_point = setup(curves_in_v, V)
        draw(V)

    def _init_curve_algorithm(self, basis, geometry, delta):
        """Initialize forward differences from basis and geometry of spline.

        Returns
        -------
            tuple : Forward differences in x and y

        """
        n = 1 / delta
        dim = basis.shape[0]
        degree = dim - 1

        spline_x = basis@np.array([p[0] for p in geometry])
        spline_y = basis@np.array([p[1] for p in geometry])

        shifts_spline_x = [spline_x.dot(np.array(
            [(i*delta)**n for n in range(degree, -1, -1)])) for i in range(dim)]
        shifts_spline_y = [spline_y.dot(np.array(
            [(i*delta)**n for n in range(degree, -1, -1)])) for i in range(dim)]

        fwd_x = init_forward_differences(shifts_spline_x)
        fwd_y = init_forward_differences(shifts_spline_y)

        return (fwd_x, fwd_y)

    def _generate_segment(self, n: 'int', basis: 'ndarray', geometry: 'ndarray'):
        """Generate cubic spline segment from geometry matrix and
        polynomial basis using forward differences.

        Notes
        -----
            The parametric curves for x and y are generated by dotting the
            change of basis matrix `basis` with the coordinates of a given
            n-degree polynomial `geometry`.

            The forward differences are calculated using the recurrence
            relation:

                D^(k)[fn+1] = D^(k)[fn] + D^(k+1)[fn]

            Lines that would cause the painter to leave the screen are
            clipped aggainst window borders. For that, it's assumed
            `clip_line` always lands on the 'one intersection' case and
            that the new point at intersection is the first of the returned
            list.

        """
        def out(x, y):
            """Test if given point is outside the window."""
            return x > 1 or x < -1 or y > 1 or y < - 1

        delta = 1 / n
        fwd_x, fwd_y = self._init_curve_algorithm(basis, geometry, delta)
        dim = basis.shape[0]

        prev_out = True
        prev_point = None
        for _ in range(n+1):
            if out(fwd_x[0], fwd_y[0]):
                if not prev_out:  # Leaving the window
                    self._cr.line_to(*self.resolution_transform(clip_line(
                        [prev_point, (fwd_x[0], fwd_y[0])])[0]))
                    self._cr.stroke()
                    prev_out = True
            else:
                if prev_out:  # Entering the window
                    if prev_point is None:
                        self._cr.move_to(*self.resolution_transform((fwd_x[0], fwd_y[0])))
                    else:
                        point_at_window = clip_line([(fwd_x[0], fwd_y[0]), prev_point])[0]
                        self._cr.move_to(*self.resolution_transform(point_at_window))
                        self._cr.line_to(*self.resolution_transform((fwd_x[0], fwd_y[0])))
                    prev_out = False
                else:  # Already inside window
                    self._cr.line_to(*self.resolution_transform((fwd_x[0], fwd_y[0])))

            prev_point = (fwd_x[0], fwd_y[0])

            for i in range(dim-1):
                fwd_x[i] += fwd_x[i+1]
                fwd_y[i] += fwd_y[i+1]
        self._cr.stroke()