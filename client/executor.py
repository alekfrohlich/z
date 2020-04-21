"""This modules provides a realization of the write-only interface to
ObjectStore.

The interface is the following:

- add: Add new object to ObjectStorage.
- remove: Remove object from ObjectStorage.
- translate: Translate object.
- scale: Scale object.
- rotate: Rotate Object.

Notes
-----
    All of the procedures realizing this interface can fail if the addressed
    object does not exist or if adding an object with a name already in use.

    Also, all procedures realizing this interface will force the viewport to
    be redrawn.

"""

import numpy as np

from util import (Logger, LogLevel)
from .objects import (Object, ObjectType)

from .object_store import ObjectStore
from .gui.viewport import Viewport


def _warn_undefined_object(method: 'function'):
    """Logs the attempt of accessing an object that does not exist."""
    def wrapper(*args, **kwargs):
        try:
            method(*args, **kwargs)
        except KeyError as e:
            Logger.log(LogLevel.ERRO, repr(e))
    return wrapper


class Executor:
    def __init__(self, obj_store: 'ObjectStore', viewport: 'Viewport'):
        """Constructs Executor."""
        self._obj_store = obj_store
        self._viewport = viewport

    @Viewport.needs_redraw
    @_warn_undefined_object
    def add(self, name: 'str', points: 'list', color=(0.0, 0.0, 0.0), t=None):
        """Attempt to add object to ObjectStore."""
        if t is None:
            t = ObjectType(3 if len(points) > 3 else len(points))
        if t is ObjectType.POLYGON:
            points.append(points[0])
        self._obj_store[name] = Object(name, points, color, t)

    @Viewport.needs_redraw
    @_warn_undefined_object
    def remove(self, name: 'str'):
        """Attempt to remove object from ObjectStore."""
        del self._obj_store[name]

    @Viewport.needs_redraw
    @_warn_undefined_object
    def translate(self, selected: 'str', dx: 'int', dy: 'int', dz: 'int'):
        """Attempt to translate point."""
        obj = self._obj_store[selected]
        obj.translate(dx, dy, dz)
        self._obj_store.changed(obj)

    @Viewport.needs_redraw
    @_warn_undefined_object
    def scale(self, selected: 'str', factor: 'int'):
        """Attempt to scale object."""
        obj = self._obj_store[selected]
        obj.scale(factor, factor, factor)
        self._obj_store.changed(obj)

    @Viewport.needs_redraw
    @_warn_undefined_object
    def rotate(self, selected: 'str', x_angle: 'float', y_angle: 'float',
               z_angle: 'float', point: 'np.array'):
        """Attempt to rotate object around of `point`."""
        obj = self._obj_store[selected]
        obj.rotate(x_angle, y_angle, z_angle, point)
        self._obj_store.changed(obj)
