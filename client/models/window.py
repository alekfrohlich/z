""""""
import numpy as np
from .paintable_object import PaintableObject
from util.linear_algebra import (translation_matrix, rotation_matrix)


class Window(PaintableObject):
    def __init__(self):
        """Construct window."""
        points = [[0, 500, 0, 1],
                  [500, 500, 0, 1],
                  [500, 0, 0, 1],
                  [0, 0, 0, 1]]
        faces = [[0, 1, 2, 3]]
        map(np.array, points)
        super().__init__("window", points, (0. ,0., 0.), 2)
        self._cached_faces = [[0, 1, 2, 3]]
        self._cached_points = [(-1, 1), (1, 1), (1, -1), (-1, -1)]
        self._orientation = np.array([[1, 0, 0, 0],
                                      [0, 1, 0, 0],
                                      [0, 0, 1, 0],
                                      [0, 0, 0, 1]])

    def __str__(self):
        return "Window with boundary: {}".format(self.points)

    @property
    def cached_faces(self) -> 'list':
        """Window's faces."""
        return self._cached_faces

    @property
    def inv_rotation_matrix(self) -> 'np.array':
        """Linear transformation that reverses orientation."""
        return np.linalg.inv(self._orientation)

    def accept(self, painter: 'ObjectPainter'):
        """Accept paint request."""
        painter.paint_polymesh(self)

    def update(self, window: 'Window'):
        """Window does not need to be updated."""
        pass

    def rotate(self, x_angle: 'float', y_angle: 'float', z_angle: 'float',
               point=None):
        """Rotate window around of `point` and update orientation."""
        if point is None:
            point = self.center
        x, y, z = point

        to_origin_tr = translation_matrix(-x, -y, -z)
        rotate_tr = rotation_matrix(x_angle, y_angle, z_angle)
        from_origin_tr = translation_matrix(x, y, z)

        self.transform(to_origin_tr@rotate_tr@from_origin_tr)
        self._orientation = self._orientation@rotate_tr
