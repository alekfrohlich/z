"""This modules provides a resizeable drawing area for drawing objects.

Classes
-------
    Viewport

"""
import cairo

from ..object_painter import ObjectPainter
from util import (Logger, LogLevel)


class Viewport:
    """Viewport class.

    The actual Gtk.DrawingArea is 20 pixels larger in both width and height
    so that the clipping algorithms implemented in this project can be tested.

    Notes
    -----
        This GUI Component handles the following signals:

        - on_draw : Gtk.Widget.signals.draw
        - on_configure : Gtk.Widget.signals.configure_event

    """

    BLACK = (0, 0, 0)
    WHITE = (1, 1, 1)

    def __init__(self, drawing_area: 'Gtk.DrawingArea',
                 obj_store: 'ObjectStore', resolution=(500, 500)):
        """Viewport constructor."""
        self._drawing_area = drawing_area
        self._obj_store = obj_store
        self._surface = None
        self._resolution = resolution
        self._drawing_area.set_size_request(
            self._resolution[0] + 20, self._resolution[1] + 20)
        self.handlers = {
            "on_draw": self._on_draw,
            "on_configure": self._on_configure,
        }

    @staticmethod
    def needs_redraw(method: 'function'):
        """Indicate that a method needs redraw to take visual effect.

        Decorate a method so that it queues a viewport redraw after
        finishing executing.

        Notes
        -----
            The decorated class must have a _viewport attribute for
            the introspection to work.

            `method` can have any number of args and kwargs.

        """
        def wrapper(cls, *args, **kwargs):
            method(cls, *args, **kwargs)
            cls._viewport._drawing_area.queue_draw()
        return wrapper

    def clear(self):
        """Clear `_surface`; paints it white."""
        cr = cairo.Context(self._surface)
        cr.set_source_rgb(*Viewport.WHITE)
        cr.paint()

    def _on_configure(self, wid: 'Gtk.Widget', evt: 'Gdk.EventConfigure'):
        """Handle on_configure signal.

        Create surface and paint it white.

        Notes
        -----
            This signal is invoked during setup and every time the
            drawing areaa resizes.

        """
        win = wid.get_window()
        width = wid.get_allocated_width()
        height = wid.get_allocated_height()
        self._surface = win.create_similar_surface(
            cairo.CONTENT_COLOR,
            width,
            height)
        self._resolution = (width - 20, height - 20)
        Logger.log(LogLevel.INFO, "viewport.config() at ({},{})"
                   .format(width, height))
        self.clear()

    def _on_draw(self, wid: 'Gtk.Widget', cr: 'Cairo.Context'):
        """Handle on_draw signal.

        Instantiate an ObjectPainter based on the drawing area's current
        resolution, and use it to paint all visible objects.

        Notes
        -----
            LineCap.ROUND is necessary for drawing points.

        """
        cr.set_source_surface(self._surface, 0, 0)
        cr.paint()
        cr.set_line_cap(cairo.LineCap.ROUND)
        painter = ObjectPainter(cr, self._resolution)
        for obj in self._obj_store.display_file:
            cr.set_source_rgb(*obj.color)
            cr.set_line_width(obj.thickness)
            obj.accept(painter)
