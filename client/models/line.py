"""This module provides a line class."""
from .paintable_object import PaintableObject
from util.clipping import clip_line


class Line(PaintableObject):
    """Line given by two points in homogeneous coordinates."""

    def __init__(self, name: 'str', points: 'list', color: 'tuple'):
        """Construct line."""
        super().__init__(name, points, color, 2)

    def __str__(self):
        """Cohersion to string."""
        return "{}(Line) at {}, with color = {}".format(
            self.name,
            str([(p[0], p[1], p[2]) for p in self._points]),
            str(self.color))

    def accept(self, painter: 'ObjectPainter'):
        """Accept paint request."""
        painter.paint_line(self)

    def update(self, window: 'Window'):
        """Update cached coordinates."""
        # self._cached_points = clip_line(self.projected(window))
        self._cached_points = self.projected(window)
        if self._cached_points:
            self._cached_points = clip_line(self._cached_points)
