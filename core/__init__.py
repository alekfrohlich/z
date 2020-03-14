""" Basic types useful for all modules. """

from enum import Enum


class DirectionType(Enum):
    UP = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    DOWN = (0, -1)


class AxisType(Enum):
    X = 1
    Y = 2
    Z = 3
