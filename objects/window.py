""" A fraction of World. """

import numpy as np

from objects.object import Object
from util.log import Logger, LogLevel

class Window(Object):
    def __init__(self, name="window", points=[
            np.array([0, 500, 1]),
            np.array([500, 500, 1]),
            np.array([500, 0, 1]),
            np.array([0, 0, 1])]):
        super().__init__("window", points, (1.0, 0.0, 0.0))
        self.angle = 0

    def rotate(self, degrees, point=None):
        super().rotate(degrees, point)
        self.angle = (self.angle + degrees) % 360

    def window_transform(self, points):
        x, y = self.center

        to_origin_tr = np.array([[1, 0, 0],
                                 [0, 1, 0],
                                 [-x, -y, 1]])

        rotate_tr = np.array([[np.cos(-self.angle), -np.sin(-self.angle), 0],
                              [np.sin(-self.angle), np.cos(-self.angle), 0],
                              [0, 0, 1]])

        vup = ((self.points[0][0] - self.points[3][0])**2 + (self.points[0][1] - self.points[3][1])**2)**0.5
        vright = ((self.points[2][0] - self.points[3][0])**2 + (self.points[2][1] - self.points[3][1])**2)**0.5

        scale_tr = np.array([[2/vup, 0, 0],
                             [0, 2/vright, 0],
                             [0, 0, 1]])

        concat_tr = to_origin_tr.dot(rotate_tr.dot(scale_tr))

        new_points = []
        for i in range(len(points)):
            new_points.append(points[i].dot(concat_tr))
        return new_points
