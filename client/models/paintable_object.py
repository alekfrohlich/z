""""""
from abc import ABCMeta, abstractmethod

from .object import Object
from util.linear_algebra import (
    translation_matrix, escalation_matrix, rotation_matrix, size, transformed)


class PaintableObject(Object):
    def __init__(self, name: 'str', points: 'list', color: 'tuple', thickness: 'float'):
        super().__init__(name, points, color, thickness)
        self._cached_points = []

    @property
    def cached_points(self) -> 'list':
        """Clipped coordinates of object (projected coordinates for curves)."""
        return self._cached_points

    @abstractmethod
    def accept(self, painter: 'ObjectPainter'): raise NotImplementedError

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
    def update(self, window: 'Window'): raise NotImplementedError

    @property
    def visible(self):
        return self.cached_points != []
