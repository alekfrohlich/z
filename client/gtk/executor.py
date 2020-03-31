""""""

from client.gtk.gui.viewport import Viewport

# @TODO: add error recovery for other semantic actions
class GtkExecutor:
    def __init__(self, obj_store, viewport):
        self._obj_store = obj_store
        self._viewport = viewport

    @Viewport.needs_redraw
    def add(self, name, points, color=(0.0, 0.0, 0.0)):
        if name == "":
            name = self.next_available_name
        self._obj_store.make_object(name, points, color)

    @Viewport.needs_redraw
    def remove(self, name):
        try:
            self._obj_store.remove_object(name)
        except KeyError as e:
            Logger.log(LogLevel.ERROR, name + " does not name an object!")

    @Viewport.needs_redraw
    def translate(self, selected, dx, dy):
        self._obj_store._display_file[selected].translate(dx, dy)

    @Viewport.needs_redraw
    def scale(self, selected, factor):
        self._obj_store._display_file[selected].scale(factor, factor)

    @Viewport.needs_redraw
    def rotate(self, selected, rads, point):
        self._obj_store._display_file[selected].rotate(rads, point)
