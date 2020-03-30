""""""

from client.clipping.cohen_sutherland import cohen_sutherland
from client.clipping.sutherland_hodgeman import sutherHodge


class WindowManager:
    def __init__(self, window):
        self._window = window

    def clip(self, points, obj_type, polygon):
        def clip_point(points):
            x, y, _ = points[0]
            if x > 1 or x < -1 or y > 1 or y < -1:
                return None
            else:
                return points

        def clip_line(points):
            return cohen_sutherland(points)

        def clip_wireframe(points):
            if polygon:
                return sutherHodge(points)
            else:
                return points

        obj_t2func = {
            1: clip_point,
            2: clip_line,
            3: clip_wireframe,
        }
        return obj_t2func[obj_type.value](self._window.window_transform(points))

    @property
    def current_window_name(self):
        return self._window.name

    @property
    def has_active_window(self):
        return self._window is not None

    def remove_window(self):
        self._window = None
