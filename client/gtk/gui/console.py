"""  """

from gi.repository.Gdk import KEY_Return, KEY_Up, KEY_Down
from gi.repository.Gtk import TextBuffer

# TODO: Accept line breaks ('\') and send resulting (possibly multi-line)
#       expressions.


class Console:
    class ConsoleBuffer(TextBuffer):
        def __init__(self):
            super().__init__()
            self.begin_line_mark = self.create_mark(
                "begin_line", self.get_start_iter(), True)
            self._unaccessible_tag = self.create_tag(
                "unaccessible_tag", editable=False, editable_set=True)
            self.insert_prompt(initial_prompt=True)

        def insert_line(self, line):
            self.delete(self.get_line_iter(), self.get_end_iter())
            self.insert_at_cursor(line)

        def insert_prompt(self, initial_prompt=False):
            self.insert_at_cursor(">> " if initial_prompt else "\n>> ")
            self.apply_tag(
                self._unaccessible_tag, self.get_start_iter(), self.get_end_iter())
            self.move_mark(self.begin_line_mark, self.get_end_iter())

        def get_line_iter(self):
            return self.get_iter_at_mark(self.begin_line_mark)

        def get_line_text(self):
            return self.get_text(
                self.get_line_iter(), self.get_end_iter(), False)


    class LineHistory:
        def __init__(self):
            self._lines = [""]
            self._scroll_index = 0

        def add_line(self, line):
            self._lines.insert(1, line)

        def down(self):
            if self._scroll_index > 0:
                self._scroll_index -= 1
            return self._lines[self._scroll_index]

        def up(self):
            if self._scroll_index < len(self._lines) - 1:
                self._scroll_index += 1
            return self._lines[self._scroll_index]

    def __init__(self, text_view, wml_interpreter):
        self._console_buff = Console.ConsoleBuffer()
        self._line_hist = Console.LineHistory()
        self._text_view = text_view
        self._wml_interpreter = wml_interpreter

        self._text_view.set_buffer(self._console_buff)
        self._text_view.connect("key-press-event", self._on_key_press)

    # Gtk signal handlers

    def _on_key_press(self, btn, event):
        stop_propagation = False
        key = event.keyval
        if key == KEY_Return:
            line = self._console_buff.get_line_text()
            self._wml_interpreter.run_line(line)
            self._console_buff.insert_prompt()
            self._line_hist.add_line(line)
            stop_propagation = True
        elif key == KEY_Up:
            self._console_buff.insert_line(self._line_hist.up())
            stop_propagation = True
        elif key == KEY_Down:
            self._console_buff.insert_line(self._line_hist.down())
            stop_propagation = True

        self._text_view.scroll_mark_onscreen(
            self._console_buff.begin_line_mark)
        return stop_propagation
