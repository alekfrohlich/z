"""This module provides an interpreter for a toy language.

The interpreter parses object manipulation language (.oml) files.
It isn't efficient, but is easier (and faster) to manipulate objects
through the console, than it is to use the graphical user interface.

The implemented commands are:
    add(name, points, faces?, bmatu?, bmatv?, color?) (*)
    translate(name, sx, sy, sz)
    scale(name, factor)
    rotate(name, x_angle, y_angle, z_angle)
    rotate_obj_axis(name, angle) (**)

(*) Parameters followed by ? are optional. Also, some are dependent on the object
    being created: faces is required for wireframes, bmatu for curves and surfaces,
    and bmatv for surfaces.

(**)
angle in degrees

The language is regular and is parsed by pattern matching.

Classes
-------
    Interpreter

"""

import re

import numpy as np

from .models import Interpolator
from util import Logger, LogLevel


name = r"[a-zA-Z]+[a-zA-Z0-9_]*"
floating = r"-?\d+.?\d*"
points = r"({0},{0},{0};)*{0},{0},{0}".format(floating) # FIXME: This regex accepts more than it should
natural = r"[0-9]+"
face = r"(({0}-)*{0})".format(natural)
faces = r"({0};)*{0}".format(face)
interpolator = r"(bezier|bspline)"
color= r"{0},{0},{0}".format(floating) # NOTE: could be restricted

NAME_PATTERN = re.compile(r"^{0}$".format(name))
POINTS_PATTERN = re.compile(r"^{0}$".format(points))

ADD_PATTERN = re.compile(  # TEMP: Do not break line earlier
    r"^add(?P<type>[clpsw])\((?P<name>{0}),(?P<points>{1})(,(?P<bmatu>{2}))?(,(?P<bmatv>{2}))?(,(?P<faces>{3}))?(,\((?P<color>{4})\))?\)$".format(
            name, points, interpolator, faces, color))

REMOVE_PATTERN = re.compile(
    r"^remove\((?P<name>{0})\)$".format(name))

TRANSLATE_PATTERN = re.compile(
    r"^translate\((?P<name>{0}),(?P<dx>{1}),(?P<dy>{1}),(?P<dz>{1})\)$".format(
        name, floating, floating))

SCALE_PATTERN = re.compile(
    r"^scale\((?P<name>{0}),(?P<factor>{1})\)$".format(name, floating))

ROTATE_PATTERN = re.compile(
    r"^rotate\((?P<name>{0}),(?P<x_angle>{1}),(?P<y_angle>{1}),(?P<z_angle>{1})\)$".format(name, floating))

ROTATEOBJAXIS_PATTERN = re.compile(
    r"^rotate_obj_axis\((?P<name>{0}),(?P<factor>{1})\)$".format(name, floating))


class Interpreter:
    """Simple interpreter for faster object manipulation."""

    def __init__(self, executor):
        """Construct interpreter."""
        self._executor = executor
        self._handler = {
            ADD_PATTERN: self._add,
            TRANSLATE_PATTERN: self._translate,
            SCALE_PATTERN: self._scale,
            ROTATE_PATTERN: self._rotate,
            REMOVE_PATTERN: self._remove,
            ROTATEOBJAXIS_PATTERN: self._rotate_obj_axis,
        }

    def faces_as_list(self, string: 'str') -> 'list':
        """Convert raw string into list of faces (each face is a pair)."""
        return [
            [int(i) for i in face.split("-")] for face in string.split(";")]

    def points_as_list(self, string: 'str') -> 'list':
        """Convert raw string of points into list of list of ndarray."""
        return [np.array([float(x), float(y), float(z), 1]) for x, y, z in map(
                lambda p: p.split(","), string.split(";"))]

    def color_as_tuple(self, string: 'str') -> 'tuple':
        """Convert raw string into triple of floats."""
        lis = re.split(r',', string)
        return (float(lis[0]), float(lis[1]), float(lis[2]))

    def interpret(self, string):
        """Interpret command by pattern matching."""
        for pattern in self._handler.keys():
            match = pattern.match(string)
            if match:
                return self._handler[pattern](match)
        Logger.log(LogLevel.WARN, "Invalid command!")

    def validate_object(self, name, points):
        """Validate object.

        Raises
        ------
            RuntimeError if name or points are not matched by NAME_PATTERN and
            POINTS_PATTERN, respectively.

        """
        if not NAME_PATTERN.match(name):
            raise RuntimeError("Invalid name!")

        if not POINTS_PATTERN.match(points):
            raise RuntimeError("Invalid list of points format!")

    def _add(self, match: 'MatchObject'):
        """Execute `add`."""
        pass
        name = match.group("name")
        points = match.group("points")
        color = match.group("color")
        if color is None:
            color = (0., 0., 0.)
        else:
            color = self.color_as_tuple(color)

        obj_type = match.group("type")
        try:
            self.validate_object(name, points)  # NOTE: Could be improved
        except RuntimeError as error:
            Logger.log(LogLevel.ERRO, error)
            return None
        params = {'name': name, 'points': self.points_as_list(points),
                  'color': color}
        if obj_type == "p":
            params['obj_type'] = "Point"
        elif obj_type == "l":
            params['obj_type'] = "Line"
        elif obj_type == "c":
            params['obj_type'] = "Curve"
            params['bmatu'] = Interpolator.BEZIER if \
                match.group("bmatu") == "bezier" else Interpolator.BSPLINE
        elif obj_type == "s":
            params['obj_type'] = "Surface"
            params['bmatu'] = Interpolator.BEZIER if \
                match.group("bmatu") == "bezier" else Interpolator.BSPLINE
            params['bmatv'] = Interpolator.BEZIER if  \
                match.group("bmatv") == "bezier" else Interpolator.BSPLINE
        elif obj_type == "w":
            params['obj_type'] = "Wireframe"
            params['faces'] = self.faces_as_list(match.group("faces"))

        self._executor.add(**params)

    def _remove(self, match):
        """Execute `remove`."""
        name = match.group("name")
        self._executor.remove(name)

    def _translate(self, match):
        """Execute `translate`."""
        name = match.group("name")
        dx = float(match.group("dx"))
        dy = float(match.group("dy"))
        dz = float(match.group("dz"))
        self._executor.translate(name, dx, dy, dz)

    def _scale(self, match):
        """Execute `scale`."""
        name = match.group("name")
        factor = float(match.group("factor"))
        self._executor.scale(name, factor)

    def _rotate(self, match):
        """Execute `rotate`."""
        name = match.group("name")
        x_angle = np.deg2rad(float(match.group("x_angle")))
        y_angle = np.deg2rad(float(match.group("y_angle")))
        z_angle = np.deg2rad(float(match.group("z_angle")))
        self._executor.rotate(name, x_angle, y_angle, z_angle, None)

    def _rotate_obj_axis(self, match):
        """Execute `rotate_obj_axis`."""
        name = match.group("name")
        angle = np.deg2rad(float(match.group("factor")))
        self._executor.rotate_obj_axis(name, angle)
