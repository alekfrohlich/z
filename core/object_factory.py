""" Object Factory and smothening optimizations. """

from models.object import Object
from models.world import World
from core.log import Logger, LogLevel


# Smoothen colinear points (>3)
class ObjectFactory:
    @staticmethod
    def make_object(name, points):
        """ Create object with given name and points, add it to the World, log
            and return it. Optmizations might be provided in the future.
        """
        obj = Object(name, points)
        Logger.log(LogLevel.INFO, obj)
        World.add_object(obj)
        return obj
