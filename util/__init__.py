"""Miscellaneous types."""

from enum import Enum


class Direction(Enum):
    """Enum representing 2D directions."""

    UP = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    DOWN = (0, -1)


class Axis(Enum):
    """Enum representing 3D Axis."""

    X = 1
    Y = 2
    Z = 3
