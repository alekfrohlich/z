""""""

from core.log import Logger, LogLevel
from gtkclient.gui.viewport import ViewPort
from models.object import Object
from models.object_factory import ObjectFactory
from models.world import World


class GtkObjectFactory(ObjectFactory):
    def __init__(self, store, viewport):
        self._store = store
        self._viewport = viewport

    @ViewPort.needs_redraw
    def make_object(self, name, points):
        if name == "":
            name = self.default_object_name()
        obj = Object(name, points)
        self._store.append([obj.name, str(obj.type)])
        World.add_object(obj)
        Logger.log(LogLevel.INFO, obj)

    def default_object_name(self):
        return "object{}".format(World.size())
