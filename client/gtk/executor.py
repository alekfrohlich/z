""""""

from util.log import Logger, LogLevel

from client.gtk.object_store import GtkObjectStore
from client.gtk.gui.viewport import Viewport


def _warn_undefined_object(method):
    def wrapper(*args, **kwargs):
        try:
            method(*args, **kwargs)
        except KeyError as e:
            Logger.log(LogLevel.ERROR, repr(e))
    return wrapper


class GtkExecutor:
    def __init__(self, obj_store, viewport):
        self._obj_store = obj_store
        self._viewport = viewport

    @Viewport.needs_redraw
    @_warn_undefined_object
    def add(self, name, points, color=(0.0, 0.0, 0.0)):
        if name == "":
            name = self.next_available_name
        self._obj_store.make_object(name, points, color)

    @Viewport.needs_redraw
    @_warn_undefined_object
    def remove(self, name):
        self._obj_store.remove_object(name)

    @Viewport.needs_redraw
    @_warn_undefined_object
    @GtkObjectStore.invalidates_cache
    def translate(self, selected, dx, dy):
        obj = self._obj_store[selected]
        obj.translate(dx, dy)
        return obj

    @Viewport.needs_redraw
    @_warn_undefined_object
    @GtkObjectStore.invalidates_cache
    def scale(self, selected, factor):
        obj = self._obj_store[selected]
        obj.scale(factor, factor)
        return obj

    @Viewport.needs_redraw
    @_warn_undefined_object
    @GtkObjectStore.invalidates_cache
    def rotate(self, selected, rads, point):
        obj = self._obj_store[selected]
        obj.rotate(rads, point)
        return obj
