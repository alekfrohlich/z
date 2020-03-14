""""""

import re
from enum import Enum

import numpy as np

from models.world import World


POINTS_PATTERN = re.compile(r"^(-?\d+,-?\d+;)*-?\d+,-?\d+$")
ADD_PATTERN = re.compile(r"^add\((-?\d+,-?\d+;)*-?\d+,-?\d+\)$")


class WML_Interpreter:
    def __init__(self, obj_factory):
        self._obj_factory = obj_factory

    def run_command(self, string):
        match = ADD_PATTERN.match(string)
        if match:
            add_expression = match.group()
            points = points_as_list(add_expression[4:len(add_expression)-1])
            self._obj_factory.make_object("", points)


def parse_points(string):
    return POINTS_PATTERN.match(string) != None

def points_as_list(string):
    """ Extract list of points (numpy arrays) from string. """
    return [
        np.array((int(point[0]), int(point[1]), 1))
        for point in map(lambda p: p.split(","),
                         string.split(";"))]
