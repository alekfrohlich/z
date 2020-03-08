""""""

from models.object import Object
from models.world import World
from core.log import Logger, LogLevel


class ObjectFactory:
    @staticmethod
    def make_object(name, points):
        obj = Object(name if name is not '' else "object{}".format(len(World.DISPLAY_FILE)), points)
        Logger.log(LogLevel.INFO, obj)
        World.add_object(obj)
        return obj
