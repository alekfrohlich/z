"""Module responsible for storing objects.

Classes
-------
    Column
    ObjectStore

"""
from enum import Enum

from gi.repository import GObject
from gi.repository import Gtk

from util import (Logger, LogLevel)
from .models import Window


class Column(Enum):
    """Enum representing the columns of underlying Gtk.ListStore."""

    OBJ = 0
    NAME = 1
    TYPE = 2


class ObjectStore(Gtk.ListStore):
    """Container for storing PaintableObjects.

    Implemented using Gtk.ListStore; provides a graphical representation of
    stored objects.

    Operations:
    - add
    - get
    - set
    - remove

    The ObjectStore also provides a list of visible objects through it's
    `display_file` property.


    See Also
    --------
        `ObjectView`

    """

    def __init__(self):
        """Construct ObjectStore.

        Specify ListStore with 3 columns: one for storing the object, another
        for storing its name, and a third for storing its type.

        Notes
        -----
            The ObjectStore is initialized with 1 object, the window.

        See also
        --------
            `Column`

        """
        Gtk.ListStore.__init__(self,
                               GObject.TYPE_PYOBJECT,
                               GObject.TYPE_STRING,
                               GObject.TYPE_STRING)
        self.window = Window()
        self["window"] = self.window

    def __getitem__(self, name: 'str') -> 'Object':
        """Retrieve object from its name.

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
        self.append([obj, obj.name, str(type(obj).__name__)])
        obj.update(self.window)
        Logger.log(LogLevel.INFO, str(obj))

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
        """Notify that the visibility of an object has changed.

        If the window is moved, all objects are updated.

        See also
        --------
            `Executor`

        """
        if obj.name == self.window.name:
            for row in self:
                o = row[Column.OBJ.value]
                o.update(self.window)
        else:
            obj.update(self.window)

    @property
    def display_file(self) -> 'list':
        """Visible objects."""
        return [row[Column.OBJ.value] for row in self
                if row[Column.OBJ.value].visible]
