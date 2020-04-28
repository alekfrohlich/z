"""This module provides C(1) composite curves.

Classes
-------
    Interpolator
    Curve

"""
import numpy as np

from .paintable_object import PaintableObject


class Interpolator:
    BEZIER = np.array([[-1,  3, -3,  1],
                       [ 3, -6,  3,  0],
                       [-3,  3,  0,  0],
                       [ 1,  0,  0,  0]])
    BSPLINE = np.array([[-1/6, 3/6, -3/6, 1/6],
                        [3/6, -6/6, 3/6, 0],
                        [-3/6, 0, 3/6, 0],
                        [1/6, 4/6, 1/6, 0]])


class Curve(PaintableObject):
    def __init__(self, name: 'str', points: 'list', bmatu: 'Interpolator',
                 color: 'tuple'):
        """Construct curve."""
        super().__init__(name, points, color, 1)
        self._bmat = bmatu

    def __str__(self):
        return "{}(Curve) with control points = {} and color = {}".format(
            self.name,
            str([(p[0], p[1], p[2]) for p in self._points]),
            str(self.color))

    @property
    def bmatu(self) -> 'Interpolator':
        """Polynomial basis used for interpolating the curve."""
        return self._bmat

    def accept(self, painter: 'ObjectPainter'):
        """Accept paint request."""
        painter.paint_curve(self)

    def update(self, window: 'Window'):
        """Generate visible parts of curve."""
        self._cached_points = self.projected(window)
