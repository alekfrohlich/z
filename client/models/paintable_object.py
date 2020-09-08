"""Augmented interface for objects that may be painted."""
from abc import abstractmethod

from .object import Object
from util.linear_algebra import (
    translation_matrix, escalation_matrix, projection_matrix, size,
    transformed)

class PaintableObject(Object):
    """"Object wrapper for painting.

    A PaintableObject is capable of putting its shape in the perspective
    of any given window. The object's points go through two steps before
    being viewport-ready:

        1. They are first projected into the 2D window using perspective
           projection, and, then,
        2. The 2D object is clipped against the window.

    It may be the case that the object is not visible through the window's
    perspective; the `visible` method is used to determine in which situation
    the object is currently in.

    The interface does not attempt to auto-detect changes to `cached_points`
    since they may be caused by the movement of another object, namely the
    window. Instead, the interface provides an update method, and relies on the
    ObjectStore to maintain the objects updated.

    The interface implements the visitor pattern, which means every
    PaintableObject may be visited by an ObjectPainter that doesn't know
    its type. Hence, the PaintableObject is responsible for calling the
    appropriate method out of the painter.

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
        def normalize(point) -> 'tuple':
            """Normalize point's coordinates in respect to the window's."""
            return (
                2*point[0]/(window_size*point[3]), 2*point[1]/(window_size*point[3]))

        # NOTE: Assumes square window
        window_size = size((window.points[0], window.points[3]))

        x, y, z = window.center
        d = window_size

        to_origin_tr = translation_matrix(-x, -y, -z)
        rotate_tr = window.inv_rotation_matrix

        cop_to_origin_tr = translation_matrix(0, 0, d)
        project_tr = projection_matrix(d)
        # concat_tr = to_origin_tr@rotate_tr@cop_to_origin_tr@project_tr
        concat_tr = to_origin_tr@rotate_tr@cop_to_origin_tr
        tr_points = transformed(self.points, concat_tr)

        for p in tr_points:
            if p[2] < d:
                return []

        return list(map(normalize, transformed(tr_points, project_tr)))

    @abstractmethod
    def update(self, window: 'Window'):
        """Update cached_points for a given window."""
        raise NotImplementedError

    @property
    def visible(self):
        return self.cached_points != []
