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
from .models import (Point, Line, Wireframe, Curve)

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

    # TEMP ====================================================================

    @Viewport.needs_redraw
    @_warn_undefined_object
    def addp(self, name: 'str', points: 'list', color=(0.0, 0.0, 0.0)):
        self._obj_store[name] = Point(name, points, color)

    @Viewport.needs_redraw
    @_warn_undefined_object
    def addl(self, name: 'str', points: 'list', color=(0.0, 0.0, 0.0)):
        self._obj_store[name] = Line(name, points, color)

    @Viewport.needs_redraw
    @_warn_undefined_object
    def addw(self, name: 'str', points: 'list', faces: 'list', color=(0.0, 0.0, 0.0)):
        self._obj_store[name] = Wireframe(name, points, faces, color)

    @Viewport.needs_redraw
    @_warn_undefined_object
    def addc(self, name: 'str', points: 'list', ctype: 'CurveType', color=(0.0, 0.0, 0.0)):
        self._obj_store[name] = Curve(name, points, ctype, color)

    # TEMP ====================================================================

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
        obj.scale(factor)
        self._obj_store.changed(obj)

    @Viewport.needs_redraw
    @_warn_undefined_object
    def rotate(self, selected: 'str', x_angle: 'float', y_angle: 'float',
               z_angle: 'float', point: 'np.array'):
        """Attempt to rotate object around of `point`."""
        obj = self._obj_store[selected]
        obj.rotate(x_angle, y_angle, z_angle, point)
        self._obj_store.changed(obj)
