"""This module contains geometric primitives.

Object types:
- Point: Defined by point.
- Line: Defined by pair of points.
- Polygon: defined by list of faces.
- Bezier: C(1) composed bezier curve.
- B-spline: Composed b-spline curve.

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


from enum import Enum

import numpy as np

from util.linear_algebra import (
    translation_matrix, escalation_matrix, rotation_matrix)


class ObjectType(Enum):
    """Enum representing possible `Object` types."""
    POINT = 1
    LINE = 2
    POLYGON = 3
    BEZIER = 4
    BSPLINE = 5

    def __str__(self):
        pretty = {
            ObjectType.POINT.value: "Point",
            ObjectType.LINE.value: "Line",
            ObjectType.POLYGON.value: "Wireframe",
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
        self._rotation_matrix = np.array([[1, 0, 0, 0],
                                          [0, 1, 0, 0],
                                          [0, 0, 1, 0],
                                          [0, 0, 0, 1]])

    def __str__(self):
        return "{}({}) with points = {} and color = {}".format(
            self.name, str(self.type), str([(p[0], p[1], p[2]) for p in self.points]), str(self.color))

    @property
    def center(self) -> 'tuple':
        """Geometric center of object."""
        # TEMP: Conversion from set to list avoids wrong computation of
        #       polygon center.
        x_points = list({point[0] for point in self.points})
        y_points = list({point[1] for point in self.points})
        z_points = list({point[2] for point in self.points})
        return (np.average(x_points), np.average(y_points), np.average(z_points))

    @property
    def inv_rotation_matrix(self) -> 'np.array':
        """Inverse rotation matrix."""
        return np.linalg.inv(self._rotation_matrix)

    def translate(self, dx: 'int', dy: 'int', dz: 'int'):
        """Translate object by (`dx`, `dy`, `dz`)."""
        self.transform(translation_matrix(dx, dy, dz))

    def scale(self, sx: 'int', sy: 'int', sz: 'int'):
        """Scale object by `sx`, `sy`, `sz` around x,y, and z-axis,
        respectively."""
        x, y, z = self.center

        to_origin_tr = translation_matrix(-x, -y, -z)
        scale_tr = escalation_matrix(sx, sy, sz)
        from_origin_tr = translation_matrix(x, y, z)

        self.transform(to_origin_tr@scale_tr@from_origin_tr)

    def rotate(self, x_angle: 'float', y_angle: 'float', z_angle: 'float',
               point=None):
        """Rotate object around of `point`."""
        if point is None:
            point = self.center
        x, y, z = point

        to_origin_tr = translation_matrix(-x, -y, -z)
        rotate_tr = rotation_matrix(x_angle, y_angle, z_angle)
        from_origin_tr = translation_matrix(x, y, z)

        self.transform(to_origin_tr@rotate_tr@from_origin_tr)
        self._rotation_matrix = self._rotation_matrix@rotate_tr

    def transform(self, matrix_tr: 'np.array'):
        """Apply `matrix_tr` to the object's coordinates."""
        for i in range(len(self.points)):
            self.points[i] = self.points[i]@matrix_tr
