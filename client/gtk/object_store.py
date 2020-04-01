""" """

# from gobject import TYPE_PYOBJECT, TYPE_STRING
from gi.repository.GObject import TYPE_PYOBJECT, TYPE_STRING
from gi.repository.Gtk import ListStore

from util.log import Logger, LogLevel
from objects.object import Object
from objects.window import Window
from client.object_store import ObjectStore


OBJ_POINTER = 0
OBJ_NAME = 1
OBJ_TYPE = 2

class GtkObjectStore(ObjectStore, ListStore):
    def __init__(self, store, window_manager):
        super().__init__(TYPE_PYOBJECT, TYPE_STRING, TYPE_STRING)
        self._window_manager = window_manager
        window_manager.set_window(self._make_window())

    def __getitem__(self, name):
        for row in self:
            if row[OBJ_NAME] == name:
                return row[OBJ_POINTER]

    def _make_window(self):
        obj = Window()
        self.append([obj, obj.name, str(obj.type)])
        Logger.log(LogLevel.INFO, obj)
        return obj

    @property
    def display_file(self):
        return [row[OBJ_POINTER] for row in self]

    @property
    def next_available_name(self):
        """ Default name for anonymous objects. """
        return "object{}".format(len(self))

    def make_object(self, name, points, color):
        """ Creates new object and adds it to the world. The returned object is
            not owned by the caller, so weird things will happen if it is
            modified. """
        if name in [row[OBJ_NAME] for row in self]:
            raise RuntimeError(name + " already names an object!")
        obj = Object(name, points, color)
        self.append([obj, obj.name, str(obj.type)])
        Logger.log(LogLevel.INFO, obj)
        return obj

    def remove_object(self, name):
        """ Removes object from the world. """
        for row in self:
            if row[OBJ_NAME] == name:
                self.remove(row.iter)
                break
        if self._window_manager.current_window_name == name:
            self._window_manager.remove_window()
        Logger.log(LogLevel.INFO, name + " has been removed!")

