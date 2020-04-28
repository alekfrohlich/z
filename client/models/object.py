"""Base class for deriving graphical objects."""
import numpy as np

from util.linear_algebra import (
    translation_matrix, escalation_matrix, rotation_matrix)


class Object:
    """"Object base class.

    Each object is composed by:
    - Name
    - List of points in 4D homogeneous coordinates.
    - RGB color tuple.
    - Thickness used for drawing.

    """

    def __init__(self, name: 'str', points: 'list', color: 'tuple',
                 thickness: 'float'):
        """Construct object."""
        self._name = name
        self._points = points
        self._color = color
        self._thickness = thickness

    @property
    def center(self) -> 'tuple':
        """Geometric center of object."""
        x_points = [point[0] for point in self.points]
        y_points = [point[1] for point in self.points]
        z_points = [point[2] for point in self.points]
        return (
            np.average(x_points), np.average(y_points), np.average(z_points))

    @property
    def color(self) -> 'tuple':
        """Color of object."""
        return self._color

    @property
    def name(self) -> 'str':
        """Name of object."""
        return self._name

    @property
    def points(self) -> 'list':
        """List of Points of object."""
        return self._points

    @property
    def thickness(self) -> 'float':
        """Thickness of object's points."""
        return self._thickness

    def translate(self, dx: 'int', dy: 'int', dz: 'int'):
        """Translate object by (`dx`, `dy`, `dz`)."""
        self.transform(translation_matrix(dx, dy, dz))

    def scale(self, factor: 'int'):
        """Scale object by factor."""
        x, y, z = self.center

        to_origin_tr = translation_matrix(-x, -y, -z)
        scale_tr = escalation_matrix(factor, factor, factor)
        from_origin_tr = translation_matrix(x, y, z)

        self.transform(to_origin_tr@scale_tr@from_origin_tr)

    def rotate(self, x_angle: 'float', y_angle: 'float', z_angle: 'float',
               point=None):
        """Rotate object around of `point`."""
        if point is None:
            point = self.center
        x, y, z = point

        to_origin_tr = translation_matrix(-x, -y, -z)
        rotate_tr = rotation_matrix(x_angle, y_angle, z_angle)
        from_origin_tr = translation_matrix(x, y, z)

        self.transform(to_origin_tr@rotate_tr@from_origin_tr)

    def transform(self, matrix_tr: 'np.array'):
        """Apply `matrix_tr` to the object's coordinates."""
        for i in range(len(self.points)):
            self.points[i] = self.points[i]@matrix_tr
