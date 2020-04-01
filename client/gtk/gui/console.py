""" Console for inputing WML commands. """

from gi.repository.Gdk import KEY_Return, KEY_Up, KEY_Down
from gi.repository.Gtk import TextBuffer

# TODO: Rename classes to: ExpressionBuffer; LineHistory; Console.
# TODO: Accept line breaks ('\') and send resulting (possibly multi-line)
#       expressions.

class CommandBuffer(TextBuffer):
    def __init__(self):
        super().__init__()
        self.begin_command_mark = self.create_mark(
            "begin_command", self.get_start_iter(), True)
        self._unaccessible_tag = self.create_tag(
            "unaccessible_tag", editable=False, editable_set=True)
        self.insert_prompt(initial_prompt=True)

    def insert_command(self, command):
        """ Override line with given command. """
        self.delete(self.get_command_iter(), self.get_end_iter())
        self.insert_at_cursor(command)

    def insert_prompt(self, initial_prompt=False):
        """ Inserts new prompt while making previously typed text not editable
            by user. """
        self.insert_at_cursor(">> " if initial_prompt else "\n>> ")
        self.apply_tag(self._unaccessible_tag, self.get_start_iter(),
                                    self.get_end_iter())
        self.move_mark(self.begin_command_mark, self.get_end_iter())

    def get_command_iter(self):
        """ Get iter at begin_command_mark. """
        return self.get_iter_at_mark(self.begin_command_mark)

    def get_command_text(self):
        """ Get last line of user-typed text.  """
        return self.get_text(self.get_command_iter(), self.get_end_iter(),
            False)


class CommandHistory:
    def __init__(self):
        self._commands = [""]
        self._scroll_index = 0

    def add_command(self, command):
        """ Add command to command history. """
        self._commands.insert(1, command)

    def down(self):
        """ Attempts to scroll down the history. Returns command at index. """
        if self._scroll_index > 0:
            self._scroll_index -= 1
        return self._commands[self._scroll_index]

    def up(self):
        """ Attempts to scroll up the history. Returns command at index. """
        if self._scroll_index < len(self._commands) - 1:
            self._scroll_index += 1
        return self._commands[self._scroll_index]


class Console:
    def __init__(self, text_view, wml_interpreter):
        self._command_buff = CommandBuffer()
        self._command_hist = CommandHistory()
        self._text_view = text_view
        self._wml_interpreter = wml_interpreter

        self._text_view.set_buffer(self._command_buff)
        self._text_view.connect("key-press-event", self._on_key_press)

    # Gtk signal handlers

    def _on_key_press(self, btn, event):
        """ Signal handler for key presses that happen while the textview has
            focus. """
        stop_propagation = False
        key = event.keyval
        if key == KEY_Return:
            command = self._command_buff.get_command_text()
            self._wml_interpreter.run_command(command)
            self._command_buff.insert_prompt()
            self._command_hist.add_command(command)
            stop_propagation = True
        elif key == KEY_Up:
            self._command_buff.insert_command(self._command_hist.up())
            stop_propagation = True
        elif key == KEY_Down:
            self._command_buff.insert_command(self._command_hist.down())
            stop_propagation = True

        self._text_view.scroll_mark_onscreen(self._command_buff.begin_command_mark)
        return stop_propagation
