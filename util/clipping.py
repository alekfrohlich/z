"""This module provides 2D clipping algorithms and ClippableObject.

Implemented algorithms (by `ObjectType`):
- Point clipping: No name.
- Line clipping: Cohen-Sutherland.
- Polygon clipping: Sutherland-Hodgeman.

ClippableObject is an adapter of Object that extends it to perfom
clipping of it's own coordinates against a given window.

Notes
-----
    All algorithms are based on a normalized coordinate system where
    the extremes of the window are at [(-1,1), (1,1), (1,-1), (-1,-1)].

See Also
--------
    `Object`
    `ObjectType`

"""
import numpy as np
from scipy import special

from client.objects import (Object, ObjectType)
from util.linear_algebra import (
    normalize_matrix, rotation_matrix, affine_transformed, normal)

# QUESTION: How to change clipping algorithm at run time? Clipper object
#           common to each type of object (one clipper for face, other for
#           curve, and another for surface).
# NOTE: The size of the object indicates if it is a point, a line, or a polygon.

class ClippableObject:
    def __init__(self, obj: 'Object', window: 'Object'):
        """Construct ClippableObject and store it's clipped coordinates."""
        self._obj = obj
        self.clipped_points = None
        self.clipping_algorithm = {
            ObjectType.POINT: clip_point,
            ObjectType.LINE: clip_line,
            ObjectType.POLYGON: clip_polygon,
            ObjectType.BEZIER: clip_bezier,
            ObjectType.BSPLINE: clip_bspline,
        }
        self.clip(window)

    def __getattr__(self, name: 'str'):
        """Provide access to the underlying object's attributes."""
        return self._obj.__getattribute__(name)

    def clip(self, window: 'Object'):
        """Update the object's `clipped_coordinates`.

        The clipping algorithms work based on the assumption of
        a normalized coordinate system where the origin lies on the
        center of the window. Thus, we begin by calculating such
        coordinates:

            1. Calculate the normal (exiting) of the window's right edge.
            2. Use atan2 to find the angle theta formed between the normal
               and the positive x-axis.
            3. Build the affine transform `window_tr` where coordinates are
               translated by the window's center, then rotated by -theta, and
               finnaly normalized.

        See also
        --------
            `__init__`
                Where the object's underlying clipping algorithm is selected.

        """
        v_up = (window.points[0], window.points[3])
        v_right = (window.points[2], window.points[3])
        x, y, z = window.center

        xn, yn = normal(window.points[1], window.points[2])
        angle = np.arctan2(yn, xn)
        rotate_tr = rotation_matrix(-angle)
        normalize_tr = normalize_matrix(v_up, v_right)

        window_tr = rotate_tr@normalize_tr
        world_coordinates = affine_transformed((x, y, z), self.points, window_tr)
        projected = project(world_coordinates)
        self.clipped_points = self.clipping_algorithm[self.type](projected)

    @property
    def visible(self) -> 'bool':
        """Wether the object is currently visible."""
        return self.clipped_points is not None


# TODO: Document clipping algorithms

def project(points: 'list') -> 'list':
    # TEMP: Where sould projection go?
    return [(p[0], p[1]) for p in points]


def clip_point(points: 'list') -> 'list':
    """Clip point by determining wether it lies inside the window."""
    x, y, z, w = points[0]
    if x > 1 or x < -1 or y > 1 or y < -1:
        return None
    else:
        return points


def clip_line(points: 'list') -> 'list':
    """Cohen-Sutherland line clipping algorithm."""
    def region_code(x, y):
        code = 0
        if x < -1:
            code += 1
        elif x > 1:
            code += 2
        if y < -1:
            code += 4
        elif y > 1:
            code += 8
        return code

    def left_intersect(x, y):
        return (-1, m * (-1 - x) + y)

    def up_intersect(x, y):
        return (x + 1/m * (1 - y), 1)

    def right_intersect(x, y):
        return (1, m * (1 - x) + y)

    def down_intersect(x, y):
        return (x + 1/m * (-1 - y), -1)

    def intersections(x, y, code):
        rc2int = {
            1: [left_intersect],
            2: [right_intersect],
            4: [down_intersect],
            5: [left_intersect, down_intersect],
            6: [right_intersect, down_intersect],
            8: [up_intersect],
            9: [left_intersect, up_intersect],
            10: [right_intersect, up_intersect],
        }
        return [i(x, y) for i in rc2int[code]]

    def valid_intersection(intersections):
        for i in intersections:
            if i[0] <= 1 and i[0] >= -1 and i[1] <= 1 and i[1] >= -1:
                return np.array([i[0], i[1], 1])
        return None

    x1, y1, z1, w1 = points[0]
    x2, y2, z2, w2 = points[1]
    rc1 = region_code(x1, y1)
    rc2 = region_code(x2, y2)
    if rc1 == 0 and rc2 == 0:  # completely inside
        return points
    elif (rc1 & rc2) != 0:  # completely outside
        return None
    else:  # partially inside
        m = (y2-y1) / (x2-x1)
        if rc1 == 0 or rc2 == 0:  # one intersection
            if rc1 != 0:
                i = valid_intersection(intersections(x1, y1, rc1))
                return (i, np.array([x2, y2, 1]))
            else:
                i = valid_intersection(intersections(x2, y2, rc2))
                return (i, np.array([x1, y1, 1]))
        else:  # possibly two intersections
            i1 = valid_intersection(intersections(x1, y1, rc1))
            i2 = valid_intersection(intersections(x2, y2, rc2))
            if i1 is None or i2 is None:  # outside
                return None
            return (i1, i2)


def clip_polygon(points):
    """Sutherland-Hodgeman polygon clipping algortihm."""
    def intersect(p1, p2, xw, yw):
        x1, y1 = p1
        x2, y2 = p2

        if x1-x2 != 0:
            m = (y1-y2) / (x1-x2)
            b = y1 - m*x1

            if yw is not None:
                xw = (yw-b)/m
            else:
                yw = m*xw + b
        else:
            if yw is not None:
                xw = x1
            else:
                pass
        return np.array([xw, yw, 1])

    xw = [-1, None, 1, None]
    yw = [None, 1, None, -1]
    border = 0

    def out(point):
        if border == 0:
            return point[0] < -1
        elif border == 1:
            return point[1] > 1
        elif border == 2:
            return point[0] > 1
        else:
            return point[1] < -1

    old_points = points
    new_points = []

    for _ in range(border, 4):
        for i in range(len(old_points) - 1):
            if out(old_points[i]) and out(old_points[i+1]):
                pass
            elif (not out(old_points[i])) and out(old_points[i+1]):
                new_points.append(intersect(
                    old_points[i], old_points[i+1], xw[border], yw[border]))
            elif out(old_points[i]) and (not out(old_points[i+1])):
                new_points.append(intersect(
                    old_points[i], old_points[i+1], xw[border], yw[border]))
                new_points.append(old_points[i+1])
            else:
                new_points.append(old_points[i+1])
        if len(new_points) != 0:
            new_points.append(new_points[0])
        old_points = new_points[:]
        new_points = []
        border += 1
    return None if old_points is [] else old_points


def out(x, y):
    """Test if given point is outside the window."""
    return x > 1 or x < -1 or y > 1 or y < - 1


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


def generate_segment(n: 'int', basis: 'np.ndarray',
                     geometry: 'np.ndarray') -> 'list':
    """Generate cubic spline segment from geometry matrix and polynomial
    basis using forward differences.

    Notes
    -----
        The parametric curves for x and y are generated by dotting the change
        of basis matrix `basis` with the coordinates of a given n-degree
        polynomial `geometry`.

        The forward differences are calculated using the recurrence relation:

            D^(k)[fn+1] = D^(k)[fn] + D^(k+1)[fn]

    """
    delta = 1 / n
    spline_x = basis@np.array([p[0] for p in geometry])
    spline_y = basis@np.array([p[1] for p in geometry])
    degree = len(spline_x) - 1

    shifts_spline_x = [spline_x.dot(np.array(
        [(i*delta)**n for n in range(3, -1, -1)])) for i in range(degree+1)]
    shifts_spline_y = [spline_y.dot(np.array(
        [(i*delta)**n for n in range(3, -1, -1)])) for i in range(degree+1)]
    fwd_x = init_forward_differences(shifts_spline_x)
    fwd_y = init_forward_differences(shifts_spline_y)

    points = [] if out(fwd_x[0], fwd_y[0]) else [(fwd_x[0], fwd_y[0])]
    for i in range(n):
        for j in range(degree):
            fwd_x[j] += fwd_x[j+1]
            fwd_y[j] += fwd_y[j+1]

        if not out(fwd_x[0], fwd_y[0]):
            points.append((fwd_x[0], fwd_y[0]))
    return points


def clip_bspline(points: 'list') -> 'list':
    """Generate visible part of B-Spline curve from n > 3 control points."""
    basis = np.array([[-1/6, 3/6, -3/6, 1/6],
                      [3/6, -6/6, 3/6, 0],
                      [-3/6, 0, 3/6, 0],
                      [1/6, 4/6, 1/6, 0]])

    clipped_points = []
    for i in range((len(points)-3)):
        clipped_points += generate_segment(100, basis, points[i:i+4])
    return clipped_points if clipped_points != [] else None


def clip_bezier(points: 'list') -> 'list':
    """Generate visible part of C(1) composite bezier curve from 4n+2 control
    points.

    Notes
    -----
        The splines are constructed as follows:

        1. The first spline uses the first 4 control points.
        2. For each two remaining points a new spline is contructed. It shares
           the last two points from it's predecessor in reverse order - if they
           were points 3 and 4 from sp_i they'll be 2 and 1 from sp_i+1.

    """
    basis = np.array([[-1,  3, -3,  1],
                      [ 3, -6,  3,  0],
                      [-3,  3,  0,  0],
                      [ 1,  0,  0,  0]])

    clipped_points = generate_segment(100, basis, points[:4])
    for i in range((len(points)-4)//2):
        geometry = [points[2*i+3], points[2*i+2], points[2*i+4], points[2*i+5]]
        clipped_points += generate_segment(100, basis, geometry)
    return clipped_points if clipped_points != [] else None
