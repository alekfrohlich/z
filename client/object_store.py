"""Module responsible for storing objects."""
from enum import Enum

import numpy as np

from gi.repository import GObject
from gi.repository import Gtk

from util import (ClippableObject, Logger, LogLevel)
from .objects import Object


class Column(Enum):
    """Enum representing the columns of the underlying Gtk.ListStore."""
    OBJ = 0
    NAME = 1
    TYPE = 2


class ObjectStore(Gtk.ListStore):
    def __init__(self):
        """Construct ObjectStore.

        Specify ListStore with 3 columns: one for storing the object, another
        for storing it's name, and a third for storing it's type.

        Notes
        -----
            The ObjectStore is initialized with 1 object, the window.

        See also
        --------
            `Column`

        """
        Gtk.ListStore.__init__(self, GObject.TYPE_PYOBJECT,
                                     GObject.TYPE_STRING,
                                     GObject.TYPE_STRING)
        points = [np.array([0, 500, 1]),
                  np.array([500, 500, 1]),
                  np.array([500, 0, 1]),
                  np.array([0, 0, 1])]
        self.window = Object("window", points, (1.0, 0.7, 0.7))
        self["window"] = self.window

    def __getitem__(self, name: 'str') -> 'Object':
        """Retrieve object from it's name.

        Raises
        ------
            KeyError
                The named object does not exist.

        """
        for row in self:
            if row[Column.NAME.value] == name:
                return row[Column.OBJ.value]
        raise KeyError(name + " does not name an object!")

    def __setitem__(self, name: 'str', obj: 'Object'):
        """Add object.

        Raises
        ------
            KeyError
                The name is already in use.

        """
        if name in [row[Column.NAME.value] for row in self]:
            raise KeyError(name + " already names an object!")
        self.append(
            [ClippableObject(obj, self.window), obj.name, str(obj.type)])
        Logger.log(LogLevel.INFO, "new object: " + str(obj))

    def __delitem__(self, name: 'str'):
        """Delete object.

        Raises
        ------
            KeyError
                The named object does not exist.

        """
        for row in self:
            if row[Column.NAME.value] == name:
                if self.window.name == name:
                    raise KeyError("cannot remove window!")
                else:
                    self.remove(row.iter)
                    Logger.log(LogLevel.INFO, name + " has been removed!")
                    return
        raise KeyError(name + " does not name an object!")

    def changed(self, obj: 'Object'):
        """Notify that an object has been changed from the outside.

        Update clipped coordinates of `obj`. If `obj` is the window,
        update all stored objects instead.

        See also
        --------
            `Executor`

        """
        if obj.name == self.window.name:
            for row in self:
                o = row[Column.OBJ.value]
                o.clip(self.window)
        else:
            obj.clip(self.window)

    @property
    def display_file(self) -> 'list':
        """Visible objects."""
        return [row[Column.OBJ.value] for row in self
                if row[Column.OBJ.value].visible]
