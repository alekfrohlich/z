"""This module provides a wireframe class."""
from .paintable_object import PaintableObject
from util.clipping import clip_wireframe


class Wireframe(PaintableObject):
    """Wireframe model using face-vertex meshes."""

    def __init__(self, name: 'str', points: 'list', faces: 'list',
                 color: 'tuple'):
        """Construct wireframe."""
        super().__init__(name, points, color, 0.1)
        self._faces = faces
        self._cached_faces = []

    def __str__(self):
        """Cohersion to string."""
        return "{}(Wire-fame) with color = {}".format(
            self.name,
            str(self.color))

    @property
    def cached_faces(self) -> 'list':
        """The Faces of clipped polygon mesh."""
        return self._cached_faces

    @property
    def faces(self) -> 'list':
        """Connected faces."""
        return self._faces

    def accept(self, painter: 'ObjectPainter'):
        """Accept paint request."""
        painter.paint_polymesh(self)

    def update(self, window: 'Window'):
        """Update cached coordinates."""
        self._cached_points, self._cached_faces = clip_wireframe(         # Clipping enabled
            self.projected(window), self.faces)                           #
        # self._cached_points = self.projected(window)                      # Clipping disabled
        # self._cached_faces = self._faces                                  #
