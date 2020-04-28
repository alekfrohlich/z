"""Augmented interface for objects that may be painted."""
from abc import abstractmethod

from .object import Object
from util.linear_algebra import (
    translation_matrix, escalation_matrix, size, transformed)


class PaintableObject(Object):
    """"Object wrapper for painting.

    Provides a screen-ready view of the Object's points: cached_points.
    The points go through two steps before being screen-ready:

        1. They are projected into the 2D window using perspective projection,
        2. The flattened object is then clipped against the window.

    The interface does not attempt to auto-detect changes, e.g., automatically
    updating the cached_points each time the object is transformed or created,
    because the most common cause of change is external: The movement of the
    window. Therefore, an `update` method is provided.

    The PaintableObject does not paint itself, indeed, PaintableObject is
    responsible for this task. The interface merely implements the visitor
    pattern, allowing ObjectPainter to identify which type of object it's
    dealling with.

    """

    def __init__(self, name: 'str', points: 'list', color: 'tuple',
                 thickness: 'float'):
        """Initialize cached points."""
        super().__init__(name, points, color, thickness)
        self._cached_points = []

    @property
    def cached_points(self) -> 'list':
        """Clipped coordinates of object (projected coordinates for curves)."""
        return self._cached_points

    @abstractmethod
    def accept(self, painter: 'ObjectPainter'):
        """Accept paint request."""
        raise NotImplementedError

    def projected(self, window) -> 'list':
        """Give the object's coordinates in respect to a given window."""
        def project(point):
            """Perspective projection."""
            return (
                point[0]*COP_DISTANCE/point[2], point[1]*COP_DISTANCE/point[2])

        # NOTE: Assumes square window
        window_size = size((window.points[0], window.points[3]))

        x, y, z = window.center
        COP_DISTANCE = 1

        to_origin_tr = translation_matrix(-x, -y, -z)
        rotate_tr = window.inv_rotation_matrix
        cop_to_origin_tr = translation_matrix(0, 0, COP_DISTANCE*window_size/2)
        scale_tr = escalation_matrix(
            2/window_size, 2/window_size, 2/window_size)
        concat_tr = to_origin_tr@rotate_tr@cop_to_origin_tr@scale_tr

        transformed_points = transformed(self.points, concat_tr)
        return list(map(project, transformed_points))

    @abstractmethod
    def update(self, window: 'Window'):
        """Update cached_points for a given window."""
        raise NotImplementedError

    @property
    def visible(self):
        return self.cached_points != []
