"""This module provides a Surface class."""
from .paintable_object import PaintableObject


class Surface(PaintableObject):
    """Surface given by control points in homogeneous coordinates."""

    def __init__(self, name: 'str', points: 'list', bmatu: 'ndarray',
                 bmatv: 'ndarray', color: 'tuple'):
        """Construct Surface."""
        super().__init__(name, points, color, 0.5)
        self._bmatu = bmatu
        self._bmatv = bmatv

    def __str__(self):
        """Cohersion to string."""
        return "{}(Surface) with control points = {} and color = {}".format(
            self.name,
            str([(p[0], p[1], p[2]) for p in self._points]),
            str(self.color))

    @property
    def bmatu(self) -> 'Interpolator':
        """interpolator for the family of curves in u."""
        return self._bmatu

    @property
    def bmatv(self) -> 'Interpolator':
        """interpolator for the family of curves in v."""
        return self._bmatv

    @property
    def degu(self) -> 'int':
        """Degree of interpolator of family of curves in u."""
        return self._bmatu.shape[0] - 1

    @property
    def degv(self) -> 'int':
        """Degree of interpolator of family of curves in v."""
        return self._bmatv.shape[0] - 1

    def accept(self, painter: 'ObjectPainter'):
        """Accept paint request."""
        painter.paint_surface(self)

    def update(self, window: 'Window'):
        """Generate visible parts of curve."""
        self._cached_points = self.projected(window)
