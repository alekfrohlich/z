""""""

import re
from enum import Enum

import numpy as np


POINTS_PATTERN = re.compile(r"^(-?\d+,-?\d+;)*-?\d+,-?\d+$")
ADD_PATTERN = re.compile(r"^add\((-?\d+,-?\d+;)*-?\d+,-?\d+\)$")


def parse_points(string):
    """ Extract list of points (numpy arrays) from string. """
    return [
        np.array((int(point[0]), int(point[1]), 1))
        for point in map(lambda p: p.split(","),
                         string.split(";"))]
