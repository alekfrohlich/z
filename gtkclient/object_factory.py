"""
    ObjectFactory that does gtkclient specific stuff:
     - Draws new object to the DrawingArea.
     - Stores the (name, type) tuple in the ListStore.
"""

from util.log import Logger, LogLevel
from objects.object import Object
from models.object_factory import ObjectFactory


class GtkObjectFactory(ObjectFactory):
    def __init__(self, store, viewport, display_file):
        self._store = store
        self._viewport = viewport
        self._display_file = display_file

    def make_object(self, name, points, color=(0.0, 0.0, 0.0)):
        """ Creates new object and adds it to the world. The returned object is
            not owned by the caller, so weird things will happen if it is
            modified. """
        if name == "":
            name = self.default_object_name()
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
        self._display_file.pop(name)
        Logger.log(LogLevel.INFO, name + " has been removed!")

    def default_object_name(self):
        """ Default name for anonymous objects. """
        return "object{}".format(len(self._display_file))
