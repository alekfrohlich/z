""" Graphical object: Point, Line or Wireframe. """

from enum import Enum

import numpy as np


class ObjectType(Enum):
    POINT = 1
    LINE = 2
    WIREFRAME = 3

    def __str__(self):
        pretty = {
            ObjectType.POINT.value: "Point",
            ObjectType.LINE.value: "Line",
            ObjectType.WIREFRAME.value: "Wireframe",
        }
        return pretty[self.value]


class Object:
    def __init__(self, name, points):
        self.name = name
        self.points = points
        self.type = ObjectType(3 if len(points) > 3 else len(points))

    def __str__(self):
        return self.name + "(" + str(self.type) + ") at " + str(self.points)

    @property
    def center(self):
        """ Center of the object. """
        x_points = [point[0] for point in self.points]
        y_points = [point[1] for point in self.points]
        return (np.average(x_points), np.average(y_points))

    def translate(self, dx, dy):
        """ Translates object by (dx, dy). """
        translate_tr = np.array([[1, 0, 0],
                              [0, 1, 0],
                              [dx, dy, 1]])
        self.transform(translate_tr)

    def scale(self, sx, sy):
        """ Scales object by sx in the x coordinate and sy in the
            y coordinate. """
        x_center, y_center = self.center

        to_origin_tr = np.array([[1, 0, 0],
                                 [0, 1, 0],
                                 [-x_center, -y_center, 1]])

        scale_tr = np.array([[sx, 0, 0],
                              [0, sy, 0],
                              [0, 0, 1]])

        from_origin_tr = np.array([[1, 0, 0],
                                   [0, 1, 0],
                                   [x_center, y_center, 1]])

        concat_tr = to_origin_tr.dot(scale_tr.dot(from_origin_tr))
        self.transform(concat_tr)

    def transform(self, matrix_tr):
        """ Applies transformation matrix to each of the object's
            coordinates. """
        for i in range(len(self.points)):
            self.points[i] = self.points[i].dot(matrix_tr)
