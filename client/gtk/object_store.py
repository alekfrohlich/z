""" """

from util.log import Logger, LogLevel
from objects.object import Object
from objects.window import Window
from client.object_store import ObjectStore


class GtkObjectStore(ObjectStore):
    def __init__(self, store, window_manager):
        self._display_file = {}
        self._store = store
        self._window_manager = window_manager
        window_manager.set_window(self._make_window())

    def _make_window(self):
        obj = Window()
        self._store.append([obj.name, str(obj.type)])
        self._display_file[obj.name] = obj
        Logger.log(LogLevel.INFO, obj)
        return obj

    @property
    def display_file(self):
        return self._display_file.values()

    @property
    def next_available_name(self):
        """ Default name for anonymous objects. """
        return "object{}".format(len(self._display_file))

    def make_object(self, name, points, color):
        """ Creates new object and adds it to the world. The returned object is
            not owned by the caller, so weird things will happen if it is
            modified. """
        if name in self._display_file:
            raise RuntimeError(name + " already names an object!")
        obj = Object(name, points, color)
        self._store.append([obj.name, str(obj.type)])
        self._display_file[name] = obj
        Logger.log(LogLevel.INFO, obj)
        return obj

    def remove_object(self, name):
        """ Removes object from the world. """
        for row in self._store:
            if row[0] == name:
                self._store.remove(row.iter)
                break
        del self._display_file[name]
        if self._window_manager.current_window_name == name:
            self._window_manager.remove_window()
        Logger.log(LogLevel.INFO, name + " has been removed!")

