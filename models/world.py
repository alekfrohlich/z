""" Conceptual representation of the world as a list of objects. """

from core.log import Logger, LogLevel
from models.object import Object


class World:
    _display_file = {}

    @staticmethod
    def make_object(name, points):
        if name is "":
            name = "object{}".format(World.size())
        obj = Object(name, points)
        Logger.log(LogLevel.INFO, obj)
        World._display_file[name] =  obj
        return obj

    @staticmethod
    def objects():
        return World._display_file

    @staticmethod
    def size():
        return len(World._display_file)
