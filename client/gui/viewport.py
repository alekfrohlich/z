"""This modules provides a drawable for drawing objects.

Classes
-------
    Viewport

"""
import cairo

from client.objects import ObjectType
from util import (Logger, LogLevel)


class Viewport:
    """Viewport class.

    The actual Gtk.DrawingArea is 20 pixels larger in both width and height
    so that the clipping algorithms implemented in this project are visible.

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
            introspection to work.

            `method` can have any number of args and kwargs.

        """
        def wrapper(cls, *args, **kwargs):
            method(cls, *args, **kwargs)
            cls._viewport._drawing_area.queue_draw()
        return wrapper

    def viewport_transform(self, point: 'tuple') -> 'tuple':
        """Change of basis from NCS to this viewport instance.

        As viewport is aligned with the window, the transform simplifies
        to a simple scaling.

        Paramters
        ---------
            point : array_like
                Array_like means all those objects -- lists, tuples, etc. --
                that can be accessed as an array of two elements

        Notes
        -----
            NCS stands for Normalized Coordinate System and it's used to
            simplificate the transform:

        x_vp = (x_w - x_wmin)/(x_wmax - x_wmin) * (x_vpmax - x_vpmin)
        y_vp = (1 - (y_w - y_wmin)/(y_wmax - y_ymin)) * (y_vpmax - y_vpmin)

            10 is added to both transformed coordinates to account for
            the clip region.

        """
        x_w, y_w = point
        x_vp = (x_w + 1) / (2) * self._resolution[0] + 10
        y_vp = (1 - (y_w + 1) / (2)) * self._resolution[1] + 10
        return (x_vp, y_vp)

    def clear(self):
        """Clear `_surface`, painting it white."""
        cr = cairo.Context(self._surface)
        cr.set_source_rgb(*Viewport.WHITE)
        cr.paint()

    def _on_configure(self, wid: 'Gtk.Widget', evt: 'Gdk.EventConfigure'):
        """Handle on_configure signal.

        Create surface and paint it white; Log viewport resolution.

        Notes
        -----
            This signal is invoked during setup and every time the
            drawing areaa resizes, however, the resolution is not
            updated for ease of debugging.

        """
        win = wid.get_window()
        width = wid.get_allocated_width()
        height = wid.get_allocated_height()
        self._surface = win.create_similar_surface(
            cairo.CONTENT_COLOR,
            width,
            height)
        Logger.log(LogLevel.INFO, "viewport.config() at ({},{})"
                   .format(width, height))
        self.clear()

    def _on_draw(self, wid: 'Gtk.Widget', cr: 'Cairo.Context'):
        """Handle on_draw signal.

        Draw all objects as follows: Start from first point and draw lines
        from every subsequent point; Connect extremes.

        Notes
        -----
            LineCap.ROUND is necessary for drawing points.

        """
        cr.set_source_surface(self._surface, 0, 0)
        cr.paint()
        cr.set_source_rgb(*Viewport.BLACK)
        cr.set_line_cap(cairo.LineCap.ROUND)

        for obj in self._obj_store.display_file:
            cr.set_source_rgb(*obj.color)
            first_point = self.viewport_transform(obj.clipped_points[0])
            cr.move_to(*first_point)
            for point in map(self.viewport_transform, obj.clipped_points):
                cr.line_to(*point)
            cr.stroke()
