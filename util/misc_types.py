"""Miscellaneous types."""
from enum import Enum


class Axis(Enum):
    """Enum representing 3D Axis."""

    X = 0
    Y = 1
    Z = 2


class Direction(Enum):
    """Enum representing 2D directions."""

    IN = (0, 0, 1)
    OUT = (0, 0, -1)
    UP = (0, 1, 0)
    LEFT = (-1, 0, 0)
    RIGHT = (1, 0, 0)
    DOWN = (0, -1, 0)
