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

from client.objects import Object
from util.linear_algebra import (
    normalize_matrix, rotation_matrix, affine_transformed, normal)

# QUESTION: How to change clipping algorithm at run time? Clipper object
#           common to each type of object (one clipper for face, other for
#           curve, and another for surface).
# NOTE: One does not need to know what specific case of a face element an
#       object is before clipping as the size of the object gives that info
#       away.


class ClippableObject:
    def __init__(self, obj: 'Object', window: 'Object'):
        """Construct ClippableObject and store it's clipped coordinates."""
        self._obj = obj
        self.clipped_points = None
        self.clipping_algorithm = clip[self.type.value]
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
        x, y = window.center

        xn, yn = normal(window.points[1], window.points[2])
        angle = np.arctan2(yn, xn)
        rotate_tr = rotation_matrix(-angle)
        normalize_tr = normalize_matrix(v_up, v_right)

        window_tr = rotate_tr@normalize_tr
        self.clipped_points = self.clipping_algorithm(
            affine_transformed((x, y), self.points, window_tr))

    @property
    def visible(self) -> 'bool':
        """Wether the object is currently visible."""
        return self.clipped_points is not None


# TODO: Document clipping algorithms


def clip_point(points: 'list') -> 'list':
    """Clip point by determining wether it lies inside the window."""
    x, y, _ = points[0]
    if x > 1 or x < -1 or y > 1 or y < -1:
        return None
    else:
        return points


def cohen_sutherland(points: 'list') -> 'list':
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

    x1, y1, _ = points[0]
    x2, y2, _ = points[1]
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


def intersect(p1, p2, xw, yw):
    x1, y1, _ = p1
    x2, y2, _ = p2

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


def sutherland_hodgeman(points):

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
    return old_points


# FIXME: Polygon clipping broken
clip = {
    1: clip_point,
    2: cohen_sutherland,
    # 3: sutherland_hodgeman,
    3: lambda p: p,
    4: lambda p: p,
}
