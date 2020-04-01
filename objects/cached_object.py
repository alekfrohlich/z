""" """

from . import object


class CachedObject(object.Object):
    def __init__(self, obj, clipped_points):
        super().__init__(obj.name, obj.points, obj.color)
        self.clipped_points = clipped_points

    @property
    def visible(self):
        return self.clipped_points is not None
