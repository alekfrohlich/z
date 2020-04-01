
from cairo import Context, LineCap, CONTENT_COLOR

from util.log import Logger, LogLevel
from client.clipping import clip


class Viewport:

    BLACK = (0, 0, 0)
    WHITE = (1, 1, 1)

    def __init__(self, drawing_area, obj_store, resolution=(500, 500)):
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
    def needs_redraw(method):
        def wrapper(cls, *args, **kwargs):
            method(cls, *args, **kwargs)
            cls._viewport._drawing_area.queue_draw()
        return wrapper

    def viewport_transform(self, point):
        x_w, y_w, _ = point
        # Add (10,10) to account for clip region!
        x_vp = (x_w + 1) / (2) * self._resolution[0] + 10
        y_vp = (1 - (y_w + 1) / (2)) * self._resolution[1] + 10
        return (x_vp, y_vp)

    def clear(self):
        cr = Context(self._surface)
        cr.set_source_rgb(*Viewport.WHITE)
        cr.paint()

    # Gtk signal handlers

    def _on_configure(self, wid, evt):
        win = wid.get_window()
        width = wid.get_allocated_width()
        height = wid.get_allocated_height()
        # self._resolution = (width, height)
        self._surface = win.create_similar_surface(
            CONTENT_COLOR,
            width,
            height)
        Logger.log(LogLevel.INFO, "viewport.config() at ({},{})"
                   .format(width, height))
        self.clear()

    def _on_draw(self, wid, cr):
        def draw_clip_region():
            cr.move_to(10, 10)
            cr.line_to(self._resolution[0] + 10, 10)
            cr.line_to(self._resolution[0] + 10, self._resolution[1] + 10)
            cr.line_to(10, self._resolution[1] + 10)
            cr.line_to(10, 10)
            cr.stroke()

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
            cr.stroke()

        def draw_placeholder():
            cr.move_to(60, 260)
            cr.set_font_size(30.0)
            cr.show_text("You are without a window!")

        cr.set_source_surface(self._surface, 0, 0)
        cr.paint()

        cr.set_line_width(2)
        cr.set_source_rgb(*Viewport.BLACK)

        obj_t2func = {
            1: draw_point,
            2: draw_line,
            3: draw_wireframe,
        }

        draw_clip_region()

        display_file = self._obj_store.display_file
        if display_file is not None:
            for obj in self._obj_store.display_file:
                cr.set_source_rgb(*obj.color)
                obj_t2func[obj.type.value](obj.clipped_points)
        else:
            draw_placeholder()
