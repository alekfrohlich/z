""" World Manipulation Language (WML)  """

import re

import numpy as np

from util import Logger, LogLevel


# NOTE: When implementing the WML Interpreter make sure that the object
#       namespace is disctinct from the variable namespace, i.e., primitives,
#       which are class methods, should be responsible for doing the look-up.


name = r"[a-zA-Z]+[a-zA-Z0-9_]*"
floating = r"-?\d+.?\d*"
points = r"({0},{0},{0};)*{0},{0},{0}".format(floating)

NAME_PATTERN = re.compile(r"^{0}$".format(name))
POINTS_PATTERN = re.compile(r"^{0}$".format(points))

ADD_PATTERN = re.compile(
    r"^add\((?P<name>{0}),(?P<points>{1})\)$".format(name, points))
TRANSLATE_PATTERN = re.compile(
    r"^translate\((?P<name>{0}),(?P<dx>{1}),(?P<dy>{1})\)$".format(
        name, floating, floating))
SCALE_PATTERN = re.compile(
    r"^scale\((?P<name>{0}),(?P<sx>{1}),(?P<sy>{1})\)$".format(name, floating))
ROTATE_PATTERN = re.compile(
    r"^rotate\((?P<name>{0}),(?P<degrees>{1}),(?P<x>{1}),(?P<y>{1})\)$".format(
        name, floating))
# INFO_PATTERN = re.compile(
#     r"^info\((?P<name>{0})\)$".format(name))
REMOVE_PATTERN = re.compile(
    r"^remove\((?P<name>{0})\)$".format(name))
# PAINT_PATTERN =  re.compile(
#     r"^paint\((?P<name>{0}),(?P<red>{1}),(?P<green>{1}),(?P<blue>{1})\)$".format(
#         name, floating, floating, floating))


class Interpreter:
    def __init__(self, executor):
        self._executor = executor
        self.executors = {
            ADD_PATTERN: self._add,
            TRANSLATE_PATTERN: self._translate,
            SCALE_PATTERN: self._scale,
            ROTATE_PATTERN: self._rotate,
            REMOVE_PATTERN: self._remove,
            # INFO_PATTERN: self._info,
            # PAINT_PATTERN: self._paint,
        }

    def points_as_list(self, string):
        return [
            np.array((float(point[0]), float(point[1]), float(point[2]), 1))
            for point in map(lambda p: p.split(","),
                             string.split(";"))]

    def color_as_tuple(self, string):
        lis = re.split(r',', string)
        return (float(lis[0]), float(lis[1]), float(lis[2]))

    def interpret(self, string):
        for pattern in self.executors.keys():
            match = pattern.match(string)
            if match:
                self.executors[pattern](match)
                return
        Logger.log(LogLevel.WARN, "Invalid command!")

    def validate_object(self, name, points):
        if not NAME_PATTERN.match(name):
            raise RuntimeError("Invalid name!")

        if not POINTS_PATTERN.match(points):
            raise RuntimeError("Invalid list of points format!")

    def _add(self, match):
        name = match.group("name")
        points = match.group("points")
        try:
            self.validate_object(name, points)
            points = self.points_as_list(points)
            self._executor.add(name, points)
        except RuntimeError as error:
            Logger.log(LogLevel.ERRO, error)

    def _remove(self, match):
        name = match.group("name")
        self._executor.remove(name)

    def _translate(self, match):
        name = match.group("name")
        dx = float(match.group("dx"))
        dy = float(match.group("dy"))
        self._executor.translate(name, dx, dy)

    def _scale(self, match):
        name = match.group("name")
        dx = float(match.group("sx"))
        dy = float(match.group("sy"))
        self._executor.scale(name, dx, dy)

    def _rotate(self, match):
        name = match.group("name")
        rads = np.deg2rad(float(match.group("degrees")))
        x = float(match.group("x"))
        y = float(match.group("y"))
        self._executor.rotate(name, rads, (x, y))

    # def _paint(self, match):
    #     """ Paints named object. """
    #     name = match.group("name")
    #     red = float(match.group("red"))
    #     green = float(match.group("green"))
    #     blue = float(match.group("blue"))
    #     self._obj_store._display_file[name].color = (red, green, blue)

    # def _info(self, match):
    #     """ Prints info. """
    #     name = match.group("name")
    #     print(self._obj_store._display_file[name])
