""" A fraction of World. """

from core.log import Logger, LogLevel


class Window:
    def __init__(self, bounds=(0, 500, 0, 500)):
        self._x_min, self._x_max, self._y_min, self._y_max = bounds

    @property
    def bounds(self):
        """ Bounds of the window. """
        return (self._x_min, self._x_max, self._y_min, self._y_max)

    def translate(self, dx, dy):
        """ Translates the window by dx and dy. """
        self._x_max += dx
        self._x_min += dx
        self._y_max += dy
        self._y_min += dy

    def scale(self, sx, sy):
        """ Scales the window by sx on x coordinates and sy on y
            coordinates. """
        new_x_max = self._x_max * sx
        new_x_min = self._x_min * sx
        new_y_max = self._y_max * sy
        new_y_min = self._x_min * sy

        if new_x_max - new_x_min < 10 or new_y_max - new_y_min < 10:
            Logger.log(LogLevel.WARN, "Zoom limited exceeded, further \
            zooming will be surpressed!")
        else:
            self._x_max = new_x_max
            self._x_min = new_x_min
            self._y_max = new_y_max
            self._y_min = new_y_min

    def rotate(self, degrees):
        """ Rotates the window by 'degrees'. """
        pass
