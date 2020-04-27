"""This module provides Surface patches."""
from .paintable_object import PaintableObject


class Surface(PaintableObject):
    """"""
    def __init__(self, name: 'str', points: 'list', bmatu: 'ndarray',
                 bmatv: 'ndarray', color: 'tuple'):
        super().__init__(name, points, color, 0.5)
        self._bmatu = bmatu
        self._bmatv = bmatv

    def __str__(self):
        return "{}(Surface) with control points = {} and color = {}".format(
            self.name,
            str([[(p[0], p[1], p[2]) for p in self._points[4*i:4*i+4]] for i in range(4)]),
            str(self.color))

    @property
    def bmatu(self) -> 'Interpolator':
        """Polynomial basis used for interpolating the family of curves in u."""
        return self._bmatu

    @property
    def bmatv(self) -> 'Interpolator':
        """Polynomial basis used for interpolating the family of curves in v."""
        return self._bmatv

    def accept(self, painter: 'ObjectPainter'):
        """Accept paint request."""
        painter.paint_surface(self)

    def update(self, window: 'Window'):
        """Generate visible parts of curve."""
        self._cached_points = self.projected(window)
