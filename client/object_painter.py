"""This module provides a way to draw the objects in the `models` package.

Classes
-------
    ObjectPainter

"""
import numpy as np
from scipy import special

from .models.curve import Interpolator
from util.clipping import clip_line


def init_forward_differences(shifts: 'list') -> 'list':
    """Initialize the first N forward differences.

    Notes
    -----
        N is the number of shifts provided as input.

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
    """Draw objects given a graphical context and the viewport's resolution."""

    def __init__(self, cr: 'Cairo.Context', resolution: 'tuple'):
        """Construct ObjectPainter."""
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
        cp = list(map(self.resolution_transform, curve.cached_points))
        if curve.bmatu is Interpolator.BEZIER:
            self._generate_segment(100, *self._init_curve_algorithm(curve.bmatu, cp[:4], 1/99))
            for i in range((len(cp) - 4) // 2):
                geometry = [cp[2*i+3], cp[2*i+2],
                            cp[2*i+4], cp[2*i+5]]
                self._generate_segment(100, *self._init_curve_algorithm(curve.bmatu, geometry, 1/99))
        else:
            for i in range(len(cp) - 3):
                self._generate_segment(100, *self._init_curve_algorithm(curve.bmatu, cp[i:i+4], 1/99))

    def paint_surface(self, surface: 'Surface'):
        """Draw bicubic bezier surface."""
        def update_fwd_diff_matrices():
            """Update forward difference matrices."""
            # //row1 <- row1 + row2
            DDx[0,:] = DDx[0,:] + DDx[1,:]
            DDy[0,:] = DDy[0,:] + DDy[1,:]
            # //row2 <- row2 + row3
            DDx[1,:] = DDx[1,:] + DDx[2,:]
            DDy[1,:] = DDy[1,:] + DDy[2,:]
            # //row3 <- row3 + row4
            DDx[2,:] = DDx[2,:] + DDx[3,:]
            DDy[2,:] = DDy[2,:] + DDy[3,:]

        rt_points = list(map(self.resolution_transform, surface._cached_points))

        Ax = np.array([[rt_points[i+4*j][0] for i in range(4)] for j in range(4)])
        Ay = np.array([[rt_points[i+4*j][1] for i in range(4)] for j in range(4)])

        Cx = surface.bmatu@Ax@np.transpose(surface.bmatu)
        Cy = surface.bmatu@Ay@np.transpose(surface.bmatu)

        n = 15
        delta = 1/ (n-1)
        Es = np.array([[0,0,0,1],
                       [delta * delta * delta, delta * delta, delta, 0],
                       [6 * delta * delta * delta, 2 * delta * delta, 0,0],
                       [6 * delta * delta * delta,0,0,0]])

        Et = np.transpose(Es)

        # Init fwd_diff matrices for t
        DDx = Es@Cx@Et
        DDy = Es@Cy@Et

        # Draw curves along t
        for i in range(n):
            self._generate_segment(n, DDx[0].copy(), DDy[0].copy())
            update_fwd_diff_matrices()

        # Init fwd_diff matrices for s
        DDx = np.transpose(Es@Cx@Et)
        DDy = np.transpose(Es@Cy@Et)

        # Draw nt curves along s
        for i in range(n):
            self._generate_segment(n, DDx[0].copy(), DDy[0].copy())
            update_fwd_diff_matrices()

    def _init_curve_algorithm(self, basis, geometry, delta) -> 'tuple':
        """Initialize forward differences from basis and geometry of spline.

        The parametric curves for x and y are generated by dotting the
        change of basis matrix `basis` with the coordinates of a given
        n-degree polynomial `geometry`.

        The forward differences are calculated using the recurrence
        relation:

                D^(k)[fn+1] = D^(k)[fn] + D^(k+1)[fn]

        Returns
        -------
            tuple : Forward differences in x and y

        """
        dim = basis.shape[0]
        degree = dim - 1

        spline_x = basis@np.array([p[0] for p in geometry])
        spline_y = basis@np.array([p[1] for p in geometry])

        shifts_spline_x = [spline_x.dot(np.array([(i*delta)**n for n in range(
            degree, -1, -1)])) for i in range(dim)]
        shifts_spline_y = [spline_y.dot(np.array([(i*delta)**n for n in range(
            degree, -1, -1)])) for i in range(dim)]

        fwd_x = init_forward_differences(shifts_spline_x)
        fwd_y = init_forward_differences(shifts_spline_y)

        return (fwd_x, fwd_y)

    def _generate_segment(self, n: 'int', fwd_x: 'list', fwd_y: 'list'):
        """Generate cubic spline segment using forward differences.

        Notes
        -----
            Lines that would cause the painter to leave the screen are
            clipped aggainst window borders. For that, it's assumed
            `clip_line` always lands on the 'one intersection' case and
            that the new point at intersection is the first of the returned
            list.

        """
        def out(x, y):
            """Test if given point is outside the window."""
            return x > self._res[0] + 10 or x < 10 or y > self._res[1] + 10 or y < 10

        res = (self._res[0]+10,10,self._res[1]+10,10)
        prev_out = True
        prev_point = None
        for _ in range(n):
            if out(fwd_x[0], fwd_y[0]):
                if not prev_out:  # Leaving the window
                    cl = clip_line([prev_point, (fwd_x[0], fwd_y[0])], *res)
                    self._cr.line_to(*cl[0])
                    self._cr.stroke()
                    prev_out = True
            else:
                if prev_out:  # Entering the window
                    if prev_point is None:
                        self._cr.move_to(fwd_x[0], fwd_y[0])
                    else:
                        point_at_window = clip_line([(fwd_x[0], fwd_y[0]), prev_point], *res)[0]
                        self._cr.move_to(*point_at_window)
                        self._cr.line_to(fwd_x[0], fwd_y[0])
                    prev_out = False
                else:  # Already inside window
                    self._cr.line_to(fwd_x[0], fwd_y[0])

            prev_point = (fwd_x[0], fwd_y[0])

            for i in range(3):
                fwd_x[i] += fwd_x[i+1]
                fwd_y[i] += fwd_y[i+1]
        self._cr.stroke()
