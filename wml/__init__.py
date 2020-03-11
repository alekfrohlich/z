""""""

import re
from enum import Enum

import numpy as np


POINTS_PATTERN = re.compile(r"^(-?\d+,-?\d+;)*-?\d+,-?\d+$")
ADD_PATTERN = re.compile(r"^add\((-?\d+,-?\d+;)*-?\d+,-?\d+\)$")


def parse_points(string):
    return [
        np.array((int(point[0]), int(point[1]), 1))
        for point in map(lambda p: p.split(","),
                         string.split(";"))]

def run_command(string):
    pass
    # match = ADD_PATTERN.match(string)
    # if match:
    #     add_expression = matches.group()
    #     points = parse_points(add_expression[4:len(add)-2])
    #     ObjectFactory.make_object("", points)
