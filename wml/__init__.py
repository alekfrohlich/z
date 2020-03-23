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
INFO_PATTERN = re.compile(
    r"^info\((?P<name>{0})\)$".format(name))
REMOVE_PATTERN = re.compile(
    r"^remove\((?P<name>{0})\)$".format(name))
COLOR_PATTERN =  re.compile(
    r"^setColor\((?P<name>{0}),(?P<red>{1}),(?P<green>{1}),(?P<blue>{1})\)$".format(
        name, floating, floating, floating))


class WML_Interpreter:
    def __init__(self, obj_factory, viewport, display_file):
        self._obj_factory = obj_factory
        self._viewport = viewport
        self._display_file = display_file
        self.executors = {
            ADD_PATTERN: self._add,
            TRANSLATE_PATTERN: self._translate,
            SCALE_PATTERN: self._scale,
            ROTATE_PATTERN: self._rotate,
            REMOVE_PATTERN: self._remove,
            INFO_PATTERN: self._info,
            COLOR_PATTERN: self._setColor,
        }

    def points_as_list(self, string):
        """ Extract list of points (numpy arrays) from string. """
        return [
            np.array((float(point[0]), float(point[1]), 1))
            for point in map(lambda p: p.split(","),
                            string.split(";"))]

    def color_as_tuple(self, string):
        lis = re.split(r',', string)
        return (float(lis[0]), float(lis[1]), float(lis[2]))

    def run_command(self, string):
        """ Runs command based on python re patterns. Thus, there is almost
            no error recovery. """
        for pattern in self.executors.keys():
            match = pattern.match(string)
            if match:
                self.executors[pattern](match)
                return
        Logger.log(LogLevel.WARN, "Invalid command!")

    def validate_object(self, name, points):
        """ Throw RuntimeError if either list of points or the chosen name is
            is badly formatted. Also checks if the name is already in use. """
        if name in self._display_file:
            raise RuntimeError(name + " already names an object!")

        if not NAME_PATTERN.match(name):
            raise RuntimeError("Invalid name!")

        if not POINTS_PATTERN.match(points):
            raise RuntimeError("Invalid list of points format!")

    @ViewPort.needs_redraw
    def _add(self, match):
        """ Adds object to the world. """
        name = match.group("name")
        points = match.group("points")
        try:
            self.validate_object(name, points)
            points = self.points_as_list(points)
            self._obj_factory.make_object(name, points)
        except RuntimeError as error:
            Logger.log(LogLevel.ERROR, error)

    @ViewPort.needs_redraw
    def _remove(self, match):
        """ Prints info. """
        name = match.group("name")
        self._obj_factory.remove_object(name)

    @ViewPort.needs_redraw
    def _translate(self, match):
        """ Translates named object. """
        name = match.group("name")
        dx = float(match.group("dx"))
        dy = float(match.group("dy"))
        self._display_file[name].translate(dx, dy)

    @ViewPort.needs_redraw
    def _scale(self, match):
        """ Scales named object. """
        name = match.group("name")
        dx = float(match.group("sx"))
        dy = float(match.group("sy"))
        self._display_file[name].scale(dx, dy)

    @ViewPort.needs_redraw
    def _rotate(self, match):
        """ Rotates named object. """
        name = match.group("name")
        degrees = np.deg2rad(float(match.group("degrees")))
        x = float(match.group("x"))
        y = float(match.group("y"))
        self._display_file[name].rotate(degrees, (x, y))

    @ViewPort.needs_redraw
    def _setColor(self, match):
        """ Rotates named object. """
        name = match.group("name")
        red = float(match.group("red"))
        green = float(match.group("green"))
        blue = float(match.group("blue"))
        self._display_file[name].setColor((red, green, blue))

    def _info(self, match):
        """ Prints info. """
        name = match.group("name")
        print(self._display_file[name])
