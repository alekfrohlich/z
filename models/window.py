""" A fraction of World. """

from core.log import Logger, LogLevel


class Window:
    x_max, y_max = (500, 500)
    x_min, y_min = (0, 0)

    @staticmethod
    def translate(dx, dy):
        """ Translates window by dx and dy. """
        Window.x_max += dx
        Window.x_min += dx
        Window.y_max += dy
        Window.y_min += dy

    @staticmethod
    def scale(sx, sy):
        """ Scales window by sx on x coordinates and sy on y coordinates. """
        new_x_max = Window.x_max * sx
        new_x_min = Window.x_min * sx
        new_y_max = Window.y_max * sy
        new_y_min = Window.x_min * sy

        if new_x_max - new_x_min < 10 or new_y_max - new_y_min < 10:
            Logger.log(LogLevel.WARN, "Zoom limited exceeded, further \
            zooming will be surpressed!")
        else:
            Window.x_max = new_x_max
            Window.x_min = new_x_min
            Window.y_max = new_y_max
            Window.y_min = new_y_min
