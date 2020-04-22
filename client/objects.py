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


# NOTE - Object Structure (Wire-frame model)
#
# The object basic structure:
#
#   Name; Points; Color;
#
# Object interface:
#
#   Name; Points; Color; Center; Translate; Scale; Rotate
#
# An object needs to be updated and drawn. In the one hand, The 'upgradable'
# requirement is an extension to Object's base interface, and thus, can be
# designed as an external interface to be inherited by Object sub-classes.
# On the other hand, the 'Drawable' requirement is not an extension, but a
# request for visitation by the Viewport. The requirements could be implemented
# using the visitor design pattern and an extended interface
#
# All object sub-classes will have a list of points, since that's the basic
# interface to transformations. However, sub-classes can add structure and
# functionality:
#
#   1. Point: thickness (float); May ignore rotations
#
#   2. Line: Nothing new
#
#   3. Wireframe: lines (list of pairs); fill (bool, not yet); renderizable
#                 (bool, not yet)
#
#   4. Curve: type (BEZIER or SPLINE); ranges (list of pairs)
#
# Each sub-class also implements it's own clipping algorithm.
#


from abc import abstractmethod, ABCMeta
from enum import Enum

import numpy as np

from util.clipping import *
from util.linear_algebra import (
    translation_matrix, escalation_matrix, rotation_matrix, size, transformed)


# NOTE: Clipping is currently disabled for Wire-frame objects
# TODO: Private attributes with public getters
#       Thickness of points
#       Fill polygons
#       Curve ranges
#       Window could return being an object (no other object needs orientation)

# TEST: point rotation

class Object:
    def __init__(self, name: 'str', points: 'list', color: 'tuple'):
        """Construct object."""
        self.name = name
        self.points = points
        self.color = color
        self._orientation = np.array([[1, 0, 0, 0],
                                      [0, 1, 0, 0],
                                      [0, 0, 1, 0],
                                      [0, 0, 0, 1]])

    def __str__(self):
        return "{} with points = {} and color = {}".format(
            self.name,
            str([(p[0], p[1], p[2]) for p in self.points]),
            str(self.color))

    @property
    def center(self) -> 'tuple':
        """Geometric center of object."""
        x_points = [point[0] for point in self.points]
        y_points = [point[1] for point in self.points]
        z_points = [point[2] for point in self.points]
        return (
            np.average(x_points), np.average(y_points), np.average(z_points))

    @property
    def inv_rotation_matrix(self) -> 'np.array':
        """Lin. Transformation that reverses _orientation."""
        return np.linalg.inv(self._orientation)

    def translate(self, dx: 'int', dy: 'int', dz: 'int'):
        """Translate object by (`dx`, `dy`, `dz`)."""
        self.transform(translation_matrix(dx, dy, dz))

    def scale(self, factor: 'int'):
        """Scale object by factor."""
        x, y, z = self.center

        to_origin_tr = translation_matrix(-x, -y, -z)
        scale_tr = escalation_matrix(factor, factor, factor)
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
        self._orientation = self._orientation@rotate_tr

    def transform(self, matrix_tr: 'np.array'):
        """Apply `matrix_tr` to the object's coordinates."""
        for i in range(len(self.points)):
            self.points[i] = self.points[i]@matrix_tr


class PaintableObject:
    __metaclass__ = ABCMeta

    @abstractmethod
    def accept(self, painter): raise NotImplementedError

    def projected(self, window) -> 'list':
        def project(point):
            """Perspective projection."""
            return (point[0]*COP_DISTANCE/point[2], point[1]*COP_DISTANCE/point[2])

        # NOTE: Assumes square window
        window_size = size((window.points[0], window.points[3]))

        x, y, z = window.center
        COP_DISTANCE = 1

        to_origin_tr = translation_matrix(-x, -y, -z)
        rotate_tr = window.inv_rotation_matrix
        cop_to_origin_tr = translation_matrix(0, 0, COP_DISTANCE*window_size/2)
        scale_tr = escalation_matrix(2/window_size, 2/window_size, 2/window_size)
        concat_tr = to_origin_tr@rotate_tr@cop_to_origin_tr@scale_tr

        transformed_points = transformed(self.points, concat_tr)
        return list(map(project, transformed_points))

    @abstractmethod
    def update(self, window): raise NotImplementedError

    @property
    def visible(self):
        return self.cached_points != []


class Point(Object, PaintableObject):
    def __init__(self, name: 'str', points: 'list', color: 'tuple'):
        """Construct point."""
        super().__init__(name, points, color)
        self._thickness = 2
        self.cached_points = []

    @property
    def thickness(self):
        """Drawing thickness."""
        return self._thickness

    def accept(self, painter: 'ObjectPainter'):
        """Accept paint request."""
        painter.paint_point(self)

    def update(self, window: 'Object'):
        """Update cached coordinates."""
        self.cached_points = clip_point(self.projected(window))

    def scale(self, factor: 'int'):
        """Scale point by increasing thickness."""
        self._thickness *= factor

    def rotate(self, x_angle: 'float', y_angle: 'float', z_angle: 'float',
               point=None):
        """Ignore rotations around center."""
        if point is not None:
            super().rotate(x_angle, y_angle, z_angle, point)


class Line(Object, PaintableObject):
    def __init__(self, name: 'str', points: 'list', color: 'tuple'):
        """Construct line."""
        super().__init__(name, points, color)

    def accept(self, painter: 'ObjectPainter'):
        """Accept paint request."""
        painter.paint_line(self)

    def update(self, window: 'Object'):
        """Update cached coordinates."""
        self.cached_points = clip_line(self.projected(window))


class Wireframe(Object, PaintableObject):
    def __init__(self, name: 'str', points: 'list', lines: 'list',
                 color: 'tuple'):
        """Construct wire-frame."""
        super().__init__(name, points, color)
        self._lines = lines
        self.cached_points = []
        self.cached_lines = []
        # TODO: Make use of:
        self._fill = False
        self._renderable = True

    @property
    def fill(self) -> 'bool':
        """Fill object with `color`?"""
        return self._fill

    @property
    def renderable(self) -> 'bool':
        """Shade and texture?"""
        return self._renderable

    @property
    def lines(self) -> 'list':
        """Connected lines."""
        return self._lines

    def accept(self, painter: 'ObjectPainter'):
        """Accept paint request."""
        painter.paint_wireframe(self)

    def update(self, window: 'Object'):
        """Update cached coordinates."""
        # self.cached_points, self.cached_lines = clip_wireframe(self.projected(window), self.lines)
        self.cached_points = self.projected(window)
        self.cached_lines = self._lines


class Curve(Object, PaintableObject):
    class CurveType:
        BEZIER = np.array([[-1,  3, -3,  1],
                           [ 3, -6,  3,  0],
                           [-3,  3,  0,  0],
                           [ 1,  0,  0,  0]])
        BSPLINE = np.array([[-1/6, 3/6, -3/6, 1/6],
                            [3/6, -6/6, 3/6, 0],
                            [-3/6, 0, 3/6, 0],
                            [1/6, 4/6, 1/6, 0]])

    def __init__(self, name: 'str', points: 'list', ctype: 'CurveType',
                 color: 'tuple'):
        """Construct curve."""
        super().__init__(name, points, color)
        self._ctype = ctype
        self.cached_points = []
        self._ranges = []

    @property
    def ctype(self):
        """Curve type."""
        return self._ctype

    @property
    def ranges(self) -> 'list':
        """Visible segments of the curve."""
        return self._ranges

    def accept(self, painter: 'ObjectPainter'):
        """Accept paint request."""
        painter.paint_curve(self)

    def update(self, window: 'Object'):
        """Generate visible parts of curve."""
        projected_points = self.projected(window)
        if self.ctype is Curve.CurveType.BEZIER:
            self.cached_points = clip_bezier(projected_points)
        else:
            self.cached_points = clip_bspline(projected_points)
