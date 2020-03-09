""" Viewport implementation using Gtk - Glade. """

from cairo import Context, CONTENT_COLOR

from core.log import Logger, LogLevel
from models.viewport import ViewPort_Common
from models.world import World


class ViewPort(ViewPort_Common):
    def __init__(self, builder):
        self._drawing_area = builder.get_object("viewport")
        self.surface = None
        self.handlers = {
            "on_draw": self._on_draw,
            "on_configure": self._on_configure,
        }

    def viewport_transform(self, objs):
        return objs

    def clear_surface(self):
        Logger.log(LogLevel.INFO, "viewport.clear_surface()")
        cr = Context(self.surface)
        cr.set_source_rgb(1, 1, 1)
        cr.paint()
        del cr

    def _on_configure(self, wid, evt):
        Logger.log(LogLevel.INFO, "Configuring viewport drawing area ...")
        if self.surface is not None:
            del self.surface
            self.surface = None
        win = wid.get_window()
        width = wid.get_allocated_width()
        height = wid.get_allocated_height()
        self.surface = win.create_similar_surface(
            CONTENT_COLOR,
            width,
            height)
        self.clear_surface()
        return True

    # Redraw the screen from the surface
    def _on_draw(self, wid, cr):
        cr.set_source_surface(self.surface, 0, 0)
        cr.paint()
        cr.set_line_width(2)
        cr.set_source_rgb(0, 0, 0)
        for obj in self.viewport_transform(World.objects()):
            points = obj.points
            cr.move_to(*points[0])
            for point in points[1:]:
                cr.line_to(*point)
        cr.stroke()
        return False

    # Shall be changed to an annotation
    def update(self):
        self._drawing_area.queue_draw()
