""""""

from enum import Enum


class ObjectType(Enum):
    POINT = 1
    LINE = 2
    WIREFRAME = 3

class Object:
    _pretty_type = {
        ObjectType.POINT: "Point",
        ObjectType.LINE: "Line",
        ObjectType.WIREFRAME: "Wireframe",
    }

    def __init__(self, name, points):
        self.name = name
        self.points = points
        self.type = ObjectType(3 if len(points) > 3 else len(points))

    def toGtkListStoreRow(self):
        return [self.name, Object._pretty_type[self.type]]

    def __str__(self):
        return self.name + "(" + Object._pretty_type[self.type] + ") at " + str(self.points)
