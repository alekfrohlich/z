""""""

import re
from enum import Enum

import numpy as np

from models.world import World


POINTS_PATTERN = re.compile(r"^(-?\d+,-?\d+;)*-?\d+,-?\d+$")
ADD_PATTERN = re.compile(r"^add\((-?\d+,-?\d+;)*-?\d+,-?\d+\)$")

# Use ObjectFactory

class WML_Interpreter:
    def __init__(self, store):
        self._store = store

    def run_command(self, string):
        match = ADD_PATTERN.match(string)
        if match:
            add_expression = match.group()
            points = parse_points(add_expression[4:len(add_expression)-2])

            obj = World.make_object("", points)
            self._store.append([obj.name, str(obj.type)])


def parse_points(string):
    """ Extract list of points (numpy arrays) from string. """
    return [
        np.array((int(point[0]), int(point[1]), 1))
        for point in map(lambda p: p.split(","),
                         string.split(";"))]
