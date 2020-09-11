"""This module provides a window class."""
import numpy as np

from .paintable_object import PaintableObject
from util.linear_algebra import (translation_matrix, rotation_matrix)


class Window(PaintableObject):
    """Square upon which other objects are projected.

    The cached points and faces are stored for compatibility
    with the PaintableObject interface; they'll never change.

    """

    def __init__(self):
        """Construct window."""
        points = [[0, 500, 0, 1],
                  [500, 500, 0, 1],
                  [500, 0, 0, 1],
                  [0, 0, 0, 1]]
        points = list(map(np.array, points))
        super().__init__("window", points, (0., 0., 0.), 2)
        self._cached_faces = [[0, 1, 2, 3]]
        self._cached_points = [(-1, 1), (1, 1), (1, -1), (-1, -1)]


    def __str__(self):
        """Cohersion to string."""
        return "Window with boundaries at {}".format(self.points)

    @property
    def cached_faces(self) -> 'list':
        """Faces."""
        return self._cached_faces

    def accept(self, painter: 'ObjectPainter'):
        """Accept paint request."""
        painter.paint_polymesh(self)

    def update(self, window: 'Window'):
        """Window does not need to be updated."""
        pass

    def rotate_obj_axis(self, angle: 'float'):
        """Window does not need to rotated around its axis."""
        pass


