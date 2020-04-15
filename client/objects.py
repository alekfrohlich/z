"""This module contains geometric objects.

Object types:
- Point: Defined by point.
- Line: Defined by pair of points.
- Sequence: Will be renamed to (parametric) curve, defined by the
            corresponding parametric generation method: Hermite, Splite, etc.
- Polygon: defined by list of faces.

Notes
-----
"""

# NOTE: Who cares about object structure: ObjStore stores objects, which
#       currently store vertices themselves. Viewport needs to know how
#       to draw object and clipper how to clip it.
# NOTE: The recursive drawing discussion currently does not make much sense,
#       it's now better to think in terms of face elements (polygons have their
#       first point repreated) and free-hand elements.
#
#           1. Face elements contain a list of points and are drawn line_to'ing
#              in linear order. Clipping is done by one of: clip_point,
#              cohen_sutherland, cohen_hodgeman, depending on the size of the
#              list of points.
#           2. Free-Hand elements contain controls and are drawn the same,
#              except for the occasional binary search for rejoining curves.
#              Clipping is done by calculating the points step by step until
#              the curve leaves the screen.
#
# Both objects cache-triggering conditions (after init and transforms) are
# equal. Thus ClippableObject can store the same 'clipped_points' in both
# cases. Drawing would too be equal in cases where the curve does not leave
# and join back the window.
# NOTE: Surfaces can be an exception to this.
# FIXME: Polygons must have their first point repeated as this would solve
#        the clipping bug and allow one mechanism to draw points, lines,
#        polygons and cubic splines.

from enum import Enum

import numpy as np

from util.linear_algebra import (
    translation_matrix, escalation_matrix, rotation_matrix)


class ObjectType(Enum):
    """Enum representing possible `Object` types."""
    POINT = 1
    LINE = 2
    WIREFRAME = 3  # FIXME: Rename to polygon
    BEZIER = 4
    BSPLINE = 5

    def __str__(self):
        pretty = {
            ObjectType.POINT.value: "Point",
            ObjectType.LINE.value: "Line",
            ObjectType.WIREFRAME.value: "Wireframe",
            ObjectType.BEZIER.value: "Bezier",
            ObjectType.BSPLINE.value: "B-Spline",
        }
        return pretty[self.value]


class Object:
    def __init__(self, name: 'str', points: 'list', color: 'tuple',
                 t: 'ObjectType'):
        """Construct object and identify it's type"""
        self.name = name
        self.points = points
        self.color = color
        self.type = t

    def __str__(self):
        return "{}({}) with points = {} and color = {}".format(
            self.name, str(self.type), str([(p[0], p[1]) for p in self.points]), str(self.color))

    @property
    def center(self) -> 'tuple':
        """Geometric center of object."""
        x_points = list({point[0] for point in self.points})
        y_points = list({point[1] for point in self.points})
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
