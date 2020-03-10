""""""


class Window:
    x_max, y_max = (500, 500)
    x_min, y_min = (0, 0)

    @staticmethod
    def move(x_offset, y_offset):
        Window.x_max += x_offset
        Window.x_min += x_offset
        Window.y_max += y_offset
        Window.y_min += y_offset
