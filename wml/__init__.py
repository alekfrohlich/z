""" World Manipulation Language (WML)  """

import re

import numpy as np

from core.log import Logger, LogLevel
from gtkclient.gui.viewport import ViewPort

name = r"[a-zA-Z]+[a-zA-Z0-9_]*"
floating = r"-?\d+.?\d*"
points = r"({0},{0};)*{0},{0}".format(floating)

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


class WML_Interpreter:
    def __init__(self, obj_factory, viewport, world):
        self._obj_factory = obj_factory
        self._viewport = viewport
        self._world = world
        self.executors = {
            ADD_PATTERN: self._add,
            TRANSLATE_PATTERN: self._translate,
            SCALE_PATTERN: self._scale,
            ROTATE_PATTERN: self._rotate,
        }

    def run_command(self, string):
        """ Runs command based on python re patterns. Thus, there is almost
            no error recovery. """
        for pattern in self.executors.keys():
            match = pattern.match(string)
            if match:
                self.executors[pattern](match)
                return
        Logger.log(LogLevel.WARN, "Invalid command!")

    @ViewPort.needs_redraw
    def _add(self, match):
        """ Adds object to the world. """
        name = match.group("name")
        points = points_as_list(match.group("points"))
        self._obj_factory.make_object(name, points)

    @ViewPort.needs_redraw
    def _translate(self, match):
        """ Translates named object. """
        name = match.group("name")
        dx = float(match.group("dx"))
        dy = float(match.group("dy"))
        self._world[name].translate(dx, dy)

    @ViewPort.needs_redraw
    def _scale(self, match):
        """ Scales named object. """
        name = match.group("name")
        dx = float(match.group("sx"))
        dy = float(match.group("sy"))
        self._world[name].scale(dx, dy)

    @ViewPort.needs_redraw
    def _rotate(self, match):
        """ Rotates named object. """
        name = match.group("name")
        degrees = float(match.group("degrees"))
        x = float(match.group("x"))
        y = float(match.group("y"))
        self._world[name].rotate(degrees, (x, y))


def parse_points(string):
    """ Tests if the string is a list of points. """
    return POINTS_PATTERN.match(string) is not None


def points_as_list(string):
    """ Extract list of points (numpy arrays) from string. """
    return [
        np.array((float(point[0]), float(point[1]), 1))
        for point in map(lambda p: p.split(","),
                         string.split(";"))]
