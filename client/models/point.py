"""This module provides a point class."""
from .paintable_object import PaintableObject
from util.clipping import clip_point


class Point(PaintableObject):
    """Point in homogeneous coordinates."""

    def __init__(self, name: 'str', points: 'list', color: 'tuple'):
        """Construct point."""
        super().__init__(name, points, color, 2)

    def __str__(self):
        """Cohersion to string."""
        return "{}(Point) at {}, with color = {}".format(
            self.name,
            str((self._points[0][0], self._points[0][1], self._points[0][2])),
            str(self.color))

    def accept(self, painter: 'ObjectPainter'):
        """Accept paint request."""
        painter.paint_point(self)

    def update(self, window: 'Window'):
        """Update cached coordinates."""
        # self._cached_points = clip_point(self.projected(window))
        self._cached_points = self.projected(window)
        if self._cached_points:
            self._cached_points = clip_point(self._cached_points)

    def scale(self, factor: 'int'):
        """A point doesn't have size, thus ignore escalations."""
        pass

    def rotate(self, x_angle: 'float', y_angle: 'float', z_angle: 'float',
               point=None):
        """Ignore rotations about center."""
        if point is not None:
            super().rotate(x_angle, y_angle, z_angle, point)
