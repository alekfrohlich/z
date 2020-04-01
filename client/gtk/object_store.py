""" """

# from gobject import TYPE_PYOBJECT, TYPE_STRING
from gi.repository.GObject import TYPE_PYOBJECT, TYPE_STRING
from gi.repository.Gtk import ListStore

from util.log import Logger, LogLevel
from objects.object import Object
from objects.cached_object import CachedObject
from objects.window import Window
from client.clipping import clip
from client.object_store import ObjectStore

# TEMP: Enum this.
OBJ_POINTER = 0
OBJ_NAME = 1
OBJ_TYPE = 2


class GtkObjectStore(ObjectStore, ListStore):
    def __init__(self):
        ListStore.__init__(self, TYPE_PYOBJECT, TYPE_STRING, TYPE_STRING)
        ObjectStore.__init__(self, self._make_window())

    def __getitem__(self, name):
        for row in self:
            if row[OBJ_NAME] == name:
                return row[OBJ_POINTER]
        raise KeyError(name + " does not name an object!")

    def _make_window(self):
        obj = Window()
        self.append([CachedObject(obj, clipped_points=None), obj.name, str(obj.type)])
        Logger.log(LogLevel.INFO, obj)
        return obj

    def _cached_points(self, obj):
        # TEMP: Will become clip[type(obj)](self._wm.to_window_coordinates(obj.points))
        return clip[obj.type.value](self._wm.to_window_coordinates(obj.points))

    @staticmethod
    def invalidates_cache(method):
        def wrapper(cls, *args, **kwargs):
            obj = method(cls, *args, **kwargs)
            if obj.name == cls._obj_store._wm.current_window_name:
                for row in cls._obj_store:
                    iter_obj = row[OBJ_POINTER]
                    iter_obj.clipped_points = cls._obj_store._cached_points(iter_obj)
            else:
                obj.clipped_points = cls._obj_store._cached_points(obj)
        return wrapper

    @property
    def display_file(self):
        if self._wm.has_active_window:
            return [row[OBJ_POINTER] for row in self if row[OBJ_POINTER].visible]
        else:
            return None

    @property
    def next_available_name(self):
        """ Default name for anonymous objects. """
        return "object{}".format(len(self))

    def make_object(self, name, points, color):
        """ Creates new object and adds it to the world. The returned object is
            not owned by the caller, so weird things will happen if it is
            modified. """
        if name in [row[OBJ_NAME] for row in self]:
            raise KeyError(name + " already names an object!")
        obj = Object(name, points, color)
        self.append([CachedObject(obj, self._cached_points(obj)), obj.name, str(obj.type)])
        Logger.log(LogLevel.INFO, obj)
        return obj

    def remove_object(self, name):
        """ Removes object from the world. """
        for row in self:
            if row[OBJ_NAME] == name:
                self.remove(row.iter)
                if self._wm.current_window_name == name:
                    self._wm.remove_window()
                Logger.log(LogLevel.INFO, name + " has been removed!")
                return
        raise KeyError(name + " does not name an object!")

