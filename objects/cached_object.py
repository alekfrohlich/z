""" """


class CachedObject:
    def __init__(self, obj, clipped_points):
        self._obj = obj
        self.clipped_points = clipped_points

    def __getattr__(self, name):
        return self._obj.__getattribute__(name)

    @property
    def visible(self):
        return self.clipped_points is not None
