"""This modules provides a drawable for drawing objects.

Classes
-------
    Viewport

"""
import cairo

from util import (Logger, LogLevel)


# NOTE: Could be moved into it's own file
class ObjectPainter:
    """"""
    def __init__(self, cr: 'Cairo.Context', resolution: 'tuple'):
        self._cr = cr
        self._res = resolution

    def resolution_transform(self, point: 'tuple') -> 'tuple':
        """Rescale points from normalized coordinate system to resolution.

        Notes
        -----
            10 is added to both transformed coordinates to account for
            the clip region.

        """
        x_w, y_w = point
        x_vp = (x_w + 1) / (2) * self._res[0] + 10
        y_vp = (1 - (y_w + 1) / (2)) * self._res[1] + 10
        return (x_vp, y_vp)

    def paint_point(self, point: 'Point'):
        self._cr.set_source_rgb(*point.color)
        p = self.resolution_transform(point.cached_points[0])
        self._cr.move_to(*p)
        self._cr.line_to(*p)
        self._cr.stroke() # QUESTION: Necessary?

    def paint_line(self, line: 'Line'):
        self._cr.set_source_rgb(*line.color)
        p0, p1 = list(map(self.resolution_transform, line.cached_points))
        self._cr.move_to(*p0)
        self._cr.line_to(*p1)
        self._cr.stroke()

    def paint_wireframe(self, wireframe: 'Wireframe'):
        self._cr.set_source_rgb(*wireframe.color)
        points = list(map(self.resolution_transform, wireframe.cached_points))
        for i, j in wireframe.cached_lines:
            self._cr.move_to(*points[i])
            self._cr.line_to(*points[j])
            self._cr.stroke()  # QUESTION: Can this be moved outside the loop?

    def paint_curve(self, curve: 'Curve'):
        self._cr.set_source_rgb(*curve.color)
        points = list(map(self.resolution_transform, curve.cached_points))
        self._cr.move_to(*points[0])
        for p in points:
            self._cr.line_to(*p)
        self._cr.stroke()

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
        cr.set_source_rgb(*Viewport.BLACK)  # QUESTION: needed?
        cr.set_line_cap(cairo.LineCap.ROUND)
        painter = ObjectPainter(cr, self._resolution)
        for obj in self._obj_store.display_file:
            obj.accept(painter)
