"""This module contains geometric objects.

Object types:
- Point: Defined by point.
- Line: Defined by pair of points.
- Sequence: Will be renamed to (parametric) curve, defined by the
            corresponding parametric generation method: Hermite, Splite, etc.
- Polygon: defined by list of points.

Notes
-----
"""

# FIXME: Currently all objects are drawn as polygons, i.e, by connecting
#        the last point to the first.
# NOTE: This wasn't previously the case; object's were drawn without connecting
#       the extremes and polygons where defined by repeting the first point.
#       This change was reverted because the .obj format expects objects to be
#       defined without repeating the last vertex.

from enum import Enum

import numpy as np

from util.linear_algebra import (
    translation_matrix, escalation_matrix, rotation_matrix)


class ObjectType(Enum):
    """Enum representing possible `Object` types."""
    POINT = 1
    LINE = 2
    SEQUENCE = 3
    POLYGON = 4

    def __str__(self):
        pretty = {
            ObjectType.POINT.value: "Point",
            ObjectType.LINE.value: "Line",
            ObjectType.SEQUENCE.value: "Sequence",
            ObjectType.POLYGON.value: "Polygon",
        }
        return pretty[self.value]


class Object:
    def __init__(self, name: 'str', points: 'list', color: 'tuple'):
        """Construct object and identify it's type"""
        self.name = name
        self.points = points
        self.color = color
        if (np.array_equal(points[0], points[len(points)-1]) and
                len(points) != 1):
            self.type = ObjectType.POLYGON
        else:
            self.type = ObjectType(3 if len(points) > 3 else len(points))

    def __str__(self):
        return self.name + "(" + str(type(self)) + ") at " + str(self.points) \
            + " with color = " + str(self.color)

    @property
    def center(self) -> 'tuple':
        """Geometric center of object."""
        x_points = [point[0] for point in self.points]
        y_points = [point[1] for point in self.points]
        return (np.average(x_points), np.average(y_points))

    def translate(self, dx: 'int', dy: 'int'):
        """Translate object by (dx, dy)."""
        self.transform(translation_matrix(dx, dy))

    def scale(self, sx: 'int', sy: 'int'):
        """Scale object by `sx` in the x-axis and `sy` in the y-axis."""
        x, y = self.center

        to_origin_tr = translation_matrix(-x, -y)
        scale_tr = escalation_matrix(sx, sy)
        from_origin_tr = translation_matrix(x, y)

        self.transform(to_origin_tr@scale_tr@from_origin_tr)

    def rotate(self, rads: 'float', point=None):
        """Rotate object by `rads` around of `point`."""
        if point is None:
            point = self.center
        x, y = point

        to_origin_tr = translation_matrix(-x, -y)
        rotate_tr = rotation_matrix(rads)
        from_origin_tr = translation_matrix(x, y)

        self.transform(to_origin_tr@rotate_tr@from_origin_tr)

    def transform(self, matrix_tr: 'np.array'):
        """Apply `matrix_tr` to the object's coordinates."""
        for i in range(len(self.points)):
            self.points[i] = self.points[i]@matrix_tr
