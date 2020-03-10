""" Viewport implementation using Gtk - Glade. """

from cairo import Context, CONTENT_COLOR

from core.log import Logger, LogLevel
from models.viewport import ViewPort_Common
from models.world import World
from models.window import Window


class ViewPort(ViewPort_Common):

    """ RBG colors for Cairo. """
    BLACK = (0, 0, 0)
    WHITE = (1, 1, 1)

    RESOLUTION = (500, 500)

    def __init__(self, builder):
        self._drawing_area = builder.get_object("viewport")
        self._surface = None
        self.handlers = {
            "on_draw": self._on_draw,
            "on_configure": self._on_configure,
        }

    @staticmethod
    def viewport_transform(point):
        """ Change of basis: World -> Viewport. """
        x_w, y_w = point
        x_vp = (x_w - Window.x_min) / (Window.x_max - Window.x_min) \
            * ViewPort.RESOLUTION[0]
        y_vp = (1 - (y_w - Window.y_min) / (Window.y_max - Window.y_min)) \
            * ViewPort.RESOLUTION[1]
        return (x_vp, y_vp)

    def clear(self):
        """ Paints the viewport white. """
        Logger.log(LogLevel.INFO, "viewport.clear()")
        cr = Context(self._surface)
        cr.set_source_rgb(*ViewPort.WHITE)
        cr.paint()

    def _on_configure(self, wid, evt):
        """ Creates surface and paint's it white. It's called at the beginning
            but will be called again whenever widget resizes. """
        win = wid.get_window()
        width = wid.get_allocated_width()
        height = wid.get_allocated_height()
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
            cr.move_to(*ViewPort.viewport_transform(points[0]))
            cr.stroke()

        def draw_line(points):
            first_point = ViewPort.viewport_transform(points[0])
            second_point = ViewPort.viewport_transform(points[1])
            cr.move_to(*first_point)
            cr.line_to(*second_point)
            cr.stroke()

        def draw_wireframe(points):
            first_point = ViewPort.viewport_transform(points[0])
            cr.move_to(*first_point)
            for point in map(ViewPort.viewport_transform, points):
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

        for obj in World.objects():
            obj_t2func[obj.type.value](obj.points)

