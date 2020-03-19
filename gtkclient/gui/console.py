""" Console for inputing WML commands. """

from gi.repository.Gdk import KEY_Return, KEY_Up, KEY_Down
from gi.repository.Gtk import TextBuffer


class CommandBuffer(TextBuffer):
    def __init__(self):
        super().__init__()
        self._begin_command_mark = self.create_mark(
            "begin_command", self.get_start_iter(), True)
        self._unaccessible_tag = self.create_tag(
            "unaccessible_tag", editable=False, editable_set=True)
        self.insert_prompt(initial_prompt=True)

    def insert_prompt(self, initial_prompt=False):
        """ Inserts new prompt while making previously typed text not editable
            by user. """
        self.insert_at_cursor(">> " if initial_prompt else "\n>> ")
        self.apply_tag(self._unaccessible_tag, self.get_start_iter(),
                                    self.get_end_iter())
        self.move_mark(self._begin_command_mark, self.get_end_iter())

    # Attributes

    @property
    def command_text(self):
        """ Last line of user-typed text.  """
        return self.get_text(self.get_iter_at_mark(
            self._begin_command_mark), self.get_end_iter(), False)


class Console:
    def __init__(self, textview, wml_interpreter):
        self._command_buff = CommandBuffer()
        self._wml_interpreter = wml_interpreter

        textview.set_buffer(self._command_buff)
        textview.connect("key-press-event", self._on_press)

    # Gtk signal handlers

    def _on_press(self, btn, event):
        """ Signal handler for key presses that happen while the textview has
            focus. """
        key = event.keyval
        if key == KEY_Return:
            self._wml_interpreter.run_command(self._command_buff.command_text)
            self._command_buff.insert_prompt()
            return True

        elif key == KEY_Up:
            print("Up!")
            return True

        elif key == KEY_Down:
            print("Down!")
            return True
