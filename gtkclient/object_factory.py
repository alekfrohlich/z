"""
    ObjectFactory that does gtkclient specific stuff:
     - Draws new object to the DrawingArea.
     - Stores the (name, type) tuple in the ListStore.
"""

from core.log import Logger, LogLevel
from gtkclient.gui.viewport import ViewPort
from models.object import Object
from models.object_factory import ObjectFactory
from models.world import World


class GtkObjectFactory(ObjectFactory):
    def __init__(self, store, viewport, world):
        self._store = store
        self._viewport = viewport
        self._world = world

    @ViewPort.needs_redraw
    def make_object(self, name, points):
        """ Creates new object and adds it to the world. The returned object is
            not owned by the caller, so weird things will happen if it is
            modified. """
        if name == "":
            name = self.default_object_name()
        obj = Object(name, points)
        self._store.append([obj.name, str(obj.type)])
        self._world.add_object(obj)
        Logger.log(LogLevel.INFO, obj)
        return obj

    def default_object_name(self):
        """ Default name for objects without it. """
        return "object{}".format(self._world.size())
