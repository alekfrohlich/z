"""This module provides a console for interpreting WML expressions.

Classes
-------
    Console
    Console.ConsoleBuffer
    Console.LineHistory

See also
--------
    `Gtk.TextView`
    `Gtk.TextBuffer`
    `wml.interpreter`
"""

from gi.repository.Gdk import KEY_Return, KEY_Up, KEY_Down
from gi.repository.Gtk import TextBuffer


class Console:
    """Text console class.

    See also
    --------
        `Gdk.KEY_Return`
        `Gdk.KEY_Up`
        `Gdk.KEY_Down`

    """

    class ConsoleBuffer(TextBuffer):
        """Class for buffering user input lines.

        The ConsoleBuffer class makes text previously typed by user
        uneditable as well as handles line breaks.

        See also
        --------
            `Gtk.TextIter`
            `Gtk.TextMark`
            `Gtk.TextTag`

        """

        def __init__(self):
            super().__init__()
            self.begin_line_mark = self.create_mark(
                "begin_line", self.get_start_iter(), True)
            self._unaccessible_tag = self.create_tag(
                "unaccessible_tag", editable=False, editable_set=True)
            self.insert_prompt(initial_prompt=True)

        def insert_line(self, line):
            """Insert line at prompt.

            See also
            --------
                `LineHistory.add_line`

            """
            self.delete(self.line_iter, self.get_end_iter())
            self.insert_at_cursor(line)

        def insert_prompt(self, initial_prompt=False):
            r"""Insert command prompt.

            Display line continuation prompt and save current line if it's
            ended by a '\'. If it is not, display regular prompt and
            discards stored lines. Also, always moves `begin_line_mark` to
            the start of the line.

            """
            if self.broken_line:
                self._expression_text += self.line_text[:-1]
                self.insert_at_cursor("\n.. ")
            else:
                self._expression_text = ""
                self.insert_at_cursor(">> " if initial_prompt else "\n>> ")
            self.apply_tag(
                self._unaccessible_tag,
                self.get_start_iter(),
                self.get_end_iter())
            self.move_mark(self.begin_line_mark, self.get_end_iter())

        @property
        def broken_line(self):
            r"""bool : Wether the last line ends in '\'."""
            if len(self.line_text) > 0:
                return self.line_text[-1] == "\\"
            else:
                return False

        @property
        def expression_text(self):
            """str : The text accumulated from `insert_prompt`."""
            return self._expression_text + self.line_text

        @property
        def line_iter(self):
            """Gtk.TextIter : iter at the begining of the currentline."""
            return self.get_iter_at_mark(self.begin_line_mark)

        @property
        def line_text(self):
            """str : Current line's text."""
            return self.get_text(
                self.line_iter, self.get_end_iter(), False)

    class LineHistory:
        """Line history; Up and Down arrows to navigate history."""

        def __init__(self):
            self._lines = [""]
            self._scroll_index = 0

        def add_line(self, line):
            """Add line at the beginning of history."""
            self._lines.insert(1, line)

        def down(self):
            """Move `scroll_index` down and return pointed line."""
            if self._scroll_index > 0:
                self._scroll_index -= 1
            return self._lines[self._scroll_index]

        def up(self):
            """Move `scroll_index` up and return pointed line."""
            if self._scroll_index < len(self._lines) - 1:
                self._scroll_index += 1
            return self._lines[self._scroll_index]

    def __init__(self, text_view, wml_interpreter):
        """Console constructor.

        Parameters
        ----------
            text_view : Gtk.TextView
            wml_interpreter : wml.Interpreter

        """
        self._console_buff = Console.ConsoleBuffer()
        self._line_hist = Console.LineHistory()
        self._text_view = text_view
        self._wml_interpreter = wml_interpreter

        self._text_view.set_buffer(self._console_buff)
        self._text_view.connect("key-press-event", self._on_key_press)

    def _on_key_press(self, btn, event):
        """Handle key-press-event from `_text_view`.

        Capture new line, up and down key strokes. New line triggers
        expression evaluation by the interpreter while up and down
        update current line's text with that from `line_hist`.

        Signals
        -------
            Gtk.Widget.signals.key_press_event

        Notes
        -----
            Gtk keeps propagating signals until a handler returns True,
            hence it's imperative that {Return, Up, Down} are intercepted
            before being inserted.

        See also
        ----------
        `Gtk.Widget.signals.key_press_event`

        """
        stop_propagation = False
        key = event.keyval
        if key == KEY_Return:
            if not self._console_buff.broken_line:
                raw = self._console_buff.expression_text
                self._wml_interpreter.interpret(raw)
            self._line_hist.add_line(self._console_buff.line_text)
            self._console_buff.insert_prompt()
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
