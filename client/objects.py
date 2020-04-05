""" """

from enum import Enum

import numpy as np


class ObjectType(Enum):
    POINT = 1
    LINE = 2
    SEQUENCE = 3
    POLYGON = 4

    def __str__(self):
        pretty = {
            ObjectType.POINT.value: "Point",
            ObjectType.LINE.value: "Line",
            ObjectType.SEQUENCE.value: "Sequence",
            ObjectType.POLYGON.value: "Polygon",
        }
        return pretty[self.value]


class Object:
    def __init__(self, name, points, color):
        self.name = name
        self.points = points
        self.color = color
        self.angle = 0
        if (np.array_equal(points[0], points[len(points)-1]) and
                len(points) != 1):
            self.type = ObjectType.POLYGON
        else:
            self.type = ObjectType(3 if len(points) > 3 else len(points))

    def __str__(self):
        return self.name + "(" + str(type(self)) + ") at " + str(self.points) \
            + " with color = " + str(self.color)

    @property
    def center(self):
        x_points = [point[0] for point in self.points]
        y_points = [point[1] for point in self.points]
        return (np.average(x_points), np.average(y_points))

    def translate(self, dx, dy):
        translate_tr = np.array([[1, 0, 0],
                                 [0, 1, 0],
                                 [dx, dy, 1]])
        self.transform(translate_tr)

    def scale(self, sx, sy):
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

    def rotate(self, rads, point=None):
        if point is None:
            point = self.center
        x, y = point

        to_origin_tr = np.array([[1, 0, 0],
                                 [0, 1, 0],
                                 [-x, -y, 1]])

        rotate_tr = np.array([[np.cos(rads), -np.sin(rads), 0],
                             [np.sin(rads), np.cos(rads), 0],
                             [0, 0, 1]])

        from_origin_tr = np.array([[1, 0, 0],
                                   [0, 1, 0],
                                   [x, y, 1]])
        concat_tr = to_origin_tr.dot(rotate_tr.dot(from_origin_tr))
        self.transform(concat_tr)
        self.angle += rads

    def in_basis(self, new_basis):
        x, y = new_basis.center

        to_origin_tr = np.array([[1, 0, 0],
                                 [0, 1, 0],
                                 [-x, -y, 1]])

        rotate_tr = np.array([[np.cos(-new_basis.angle), -np.sin(-new_basis.angle), 0],
                              [np.sin(-new_basis.angle), np.cos(-new_basis.angle), 0],
                              [0, 0, 1]])

        change_of_basis_tr = to_origin_tr.dot(rotate_tr)
        return change_of_basis_tr

    def normalized(self, reference):
        vup = ((reference.points[0][0] - reference.points[3][0])**2 +
               (reference.points[0][1] - reference.points[3][1])**2)**0.5
        vright = ((reference.points[2][0] - reference.points[3][0])**2 +
                  (reference.points[2][1] - reference.points[3][1])**2)**0.5

        scale_tr = np.array([[2/vup, 0, 0],
                             [0, 2/vright, 0],
                             [0, 0, 1]])
        return scale_tr

    def transform(self, matrix_tr):
        for i in range(len(self.points)):
            self.points[i] = self.points[i].dot(matrix_tr)

    def transformed(self, matrix_tr):
        new_points = []
        for i in range(len(self.points)):
            new_points.append(self.points[i].dot(matrix_tr))
        return new_points