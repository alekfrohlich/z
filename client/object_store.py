""" """

from enum import Enum

import numpy as np

from gi.repository.GObject import TYPE_PYOBJECT, TYPE_STRING
from gi.repository.Gtk import ListStore

from util import ClippedObject, Logger, LogLevel
from .objects import Object


class Column(Enum):
    OBJ = 0
    NAME = 1
    TYPE = 2


class ObjectStore(ListStore):
    def __init__(self):
        ListStore.__init__(self, TYPE_PYOBJECT, TYPE_STRING, TYPE_STRING)
        points = [np.array([0, 500, 1]),
            np.array([500, 500, 1]),
            np.array([500, 0, 1]),
            np.array([0, 0, 1])]
        self.window = Object("window", points, (1.0, 0.7, 0.7))
        self["window"] = self.window
        Logger.log(LogLevel.INFO, self.window)

    def __getitem__(self, name):
        for row in self:
            if row[Column.NAME.value] == name:
                return row[Column.OBJ.value]
        raise KeyError(name + " does not name an object!")

    def __setitem__(self, name, obj):
        if name in [row[Column.NAME.value] for row in self]:
            raise KeyError(name + " already names an object!")
        self.append([ClippedObject(obj, self.window), obj.name, str(obj.type)])
        Logger.log(LogLevel.INFO, "new object: " + str(obj))

    def __delitem__(self, name):
        for row in self:
            if row[Column.NAME.value] == name:
                if self.window.name == name:
                    raise KeyError("cannot remove window!")
                else:
                    self.remove(row.iter)
                    Logger.log(LogLevel.INFO, name + " has been removed!")
                    return
        raise KeyError(name + " does not name an object!")

    def changed(self, obj):
        if obj.name == self.window.name:
            for row in self:
                o = row[Column.OBJ.value]
                o.clip(self.window)
        else:
            obj.clip(self.window)

    @property
    def display_file(self):
        return [row[Column.OBJ.value] for row in self
                if row[Column.OBJ.value].visible]
