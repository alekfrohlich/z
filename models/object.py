""" Graphical object: Point, Line or Wireframe. """

from enum import Enum


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
