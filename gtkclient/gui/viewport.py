""" Vector graphics viewport using cairo. It's starting resolution is of
    500x500, but can be dynamically resized. """

from cairo import Context, LineCap, CONTENT_COLOR

from core.log import Logger, LogLevel
from models.world import World


class ViewPort:

    """ RBG colors for Cairo. """
    BLACK = (0, 0, 0)
    WHITE = (1, 1, 1)

    def __init__(self, builder, window, world):
        self._drawing_area = builder.get_object("viewport")
        self._surface = None
        self._window = window
        self._world = world
        self._resolution = (500, 500)
        self.handlers = {
            "on_draw": self._on_draw,
            "on_configure": self._on_configure,
        }

    @staticmethod
    def needs_redraw(method):
        """ Decorates methods of any class that has a _viewport attribute
            (Viewport instace) so that any changes made to the displayfile are
            visible in the viewport. """
        def wrapper(cls, *args, **kwargs):
            method(cls, *args, **kwargs)
            cls._viewport._drawing_area.queue_draw()
        return wrapper

    def viewport_transform(self, point):
        """ Change of basis: World -> Viewport. """
        x_w, y_w, _ = point
        x_win_min, x_win_max, y_win_min, y_win_max = self._window.bounds
        x_vp = (x_w - x_win_min) / (x_win_max - x_win_min) \
            * self._resolution[0]
        y_vp = (1 - (y_w - y_win_min) / (y_win_max - y_win_min)) \
            * self._resolution[1]
        return (x_vp, y_vp)

    def clear(self):
        """ Paints the viewport white. """
        cr = Context(self._surface)
        cr.set_source_rgb(*ViewPort.WHITE)
        cr.paint()

    # Gtk signal handlers

    def _on_configure(self, wid, evt):
        """ Creates surface and paint's it white. It's called at the beginning
            but will be called again whenever widget resizes. """
        win = wid.get_window()
        width = wid.get_allocated_width()
        height = wid.get_allocated_height()
        self._resolution = (width, height)
        self._surface = win.create_similar_surface(
            CONTENT_COLOR,
            width,
            height)
        Logger.log(LogLevel.INFO, "viewport.config() at ({},{})"
                   .format(width, height))
        self.clear()

    def _on_draw(self, wid, cr):
        """ Redraws the screen from the surface. """
        def draw_point(points):
            cr.move_to(*self.viewport_transform(points[0]))
            cr.set_line_cap(LineCap.ROUND)
            cr.close_path()
            cr.stroke()

        def draw_line(points):
            first_point = self.viewport_transform(points[0])
            second_point = self.viewport_transform(points[1])
            cr.move_to(*first_point)
            cr.line_to(*second_point)
            cr.stroke()

        def draw_wireframe(points):
            first_point = self.viewport_transform(points[0])
            cr.move_to(*first_point)
            for point in map(self.viewport_transform, points):
                cr.line_to(*point)
            cr.line_to(*first_point)
            cr.stroke()

        cr.set_source_surface(self._surface, 0, 0)
        cr.paint()

        cr.set_line_width(2)
        cr.set_source_rgb(*ViewPort.BLACK)

        obj_t2func = {
            1: draw_point,
            2: draw_line,
            3: draw_wireframe,
        }

        for obj in self._world.objects().values():
            obj_t2func[obj.type.value](obj.points)
