""""""

from util import Logger, LogLevel
from .objects import Object

from .object_store import ObjectStore
from .gui.viewport import Viewport


def _warn_undefined_object(method):
    def wrapper(*args, **kwargs):
        try:
            method(*args, **kwargs)
        except KeyError as e:
            Logger.log(LogLevel.ERRO, repr(e))
    return wrapper


class GtkExecutor:
    def __init__(self, obj_store, viewport):
        self._obj_store = obj_store
        self._viewport = viewport

    @Viewport.needs_redraw
    @_warn_undefined_object
    def add(self, name, points, color=(0.0, 0.0, 0.0)):
        self._obj_store[name] = Object(name, points, color)

    @Viewport.needs_redraw
    @_warn_undefined_object
    def remove(self, name):
        del self._obj_store[name]

    @Viewport.needs_redraw
    @_warn_undefined_object
    def translate(self, selected, dx, dy):
        obj = self._obj_store[selected]
        obj.translate(dx, dy)
        self._obj_store.changed(obj)

    @Viewport.needs_redraw
    @_warn_undefined_object
    def scale(self, selected, factor):
        obj = self._obj_store[selected]
        obj.scale(factor, factor)
        self._obj_store.changed(obj)

    @Viewport.needs_redraw
    @_warn_undefined_object
    def rotate(self, selected, rads, point):
        obj = self._obj_store[selected]
        obj.rotate(rads, point)
        self._obj_store.changed(obj)
