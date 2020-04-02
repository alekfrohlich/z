""" """

from enum import Enum

from gi.repository.GObject import TYPE_PYOBJECT, TYPE_STRING
from gi.repository.Gtk import ListStore

from util.log import Logger, LogLevel
from objects.cached_object import CachedObject
from objects.window import Window

from ..clipping import clip
from ..object_store import ObjectStore


class Column(Enum):
    OBJ = 0
    NAME = 1
    TYPE = 2


class GtkObjectStore(ObjectStore, ListStore):
    def __init__(self):
        ListStore.__init__(self, TYPE_PYOBJECT, TYPE_STRING, TYPE_STRING)
        window = Window()
        self.append([CachedObject(
            window, clipped_points=None), window.name, str(window.type)])
        Logger.log(LogLevel.INFO, window)
        ObjectStore.__init__(self, window)

    # Container interface

    def __getitem__(self, name):
        for row in self:
            if row[Column.NAME.value] == name:
                return row[Column.OBJ.value]
        raise KeyError(name + " does not name an object!")

    def __setitem__(self, name, obj):
        if name in [row[Column.NAME.value] for row in self]:
            raise KeyError(name + " already names an object!")
        self.append([CachedObject(
                obj, self._cached_points(obj)), obj.name, str(obj.type)])
        Logger.log(LogLevel.INFO, "new object: " + str(obj))

    def __delitem__(self, name):
        for row in self:
            if row[Column.NAME.value] == name:
                self.remove(row.iter)
                if self._wm.current_window_name == name:
                    self._wm.remove_window()
                Logger.log(LogLevel.INFO, name + " has been removed!")
                return
        raise KeyError(name + " does not name an object!")

    def _cached_points(self, obj):
        return clip[obj.type.value](self._wm.to_window_coordinates(obj.points))

    @staticmethod
    def invalidates_cache(method):
        def wrapper(cls, *args, **kwargs):
            obj = method(cls, *args, **kwargs)
            if obj.name == cls._obj_store._wm.current_window_name:
                for row in cls._obj_store:
                    iter_obj = row[Column.OBJ.value]
                    iter_obj.clipped_points = cls._obj_store._cached_points(
                        iter_obj)
            else:
                obj.clipped_points = cls._obj_store._cached_points(obj)
        return wrapper

    @property
    def display_file(self):
        if self._wm.has_active_window:
            return [row[Column.OBJ.value] for row in self
                    if row[Column.OBJ.value].visible]
        else:
            return None
