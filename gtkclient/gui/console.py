""" Console for inputing WML commands. """


class Console:
    def __init__(self, text_buffer, wml_interpreter):
        self._text_buffer = text_buffer
        self._wml_interpreter = wml_interpreter
        self._on_insert_text_handler_id = self._text_buffer.connect(
            "insert-text", self._on_insert_text)
        self._begin_command_mark = self._text_buffer.create_mark(
            "begin_command", self._start, True)
        self._unaccessible_tag = self._text_buffer.create_tag("unaccessible_tag", editable=False, editable_set=True)
        self._insert_prompt()

    def _insert_prompt(self):
        """ Inserts new prompt while making previously typed text not editable
            by user. """
        self._text_buffer.insert_at_cursor(">> ")
        self._text_buffer.apply_tag(self._unaccessible_tag, self._start,
            self._end)
        self._text_buffer.move_mark(self._begin_command_mark, self._end)

    # Attributes

    @property
    def command_text(self):
        """ Last line of user-typed text.  """
        return self._text_buffer.get_text(self._text_buffer.get_iter_at_mark(
            self._begin_command_mark), self._end, False)

    @property
    def _start(self):
        """ Start of buffer TextIter (Gtk). """
        return self._text_buffer.get_start_iter()

    @property
    def _end(self):
        """ End of buffer TextIter (Gtk). """
        return self._text_buffer.get_end_iter()

    # Gtk signal handlers

    def _on_insert_text(self, buff, location, text, length):
        """ If the user finished typing a line, forwards such line to the
            WML interpreter to process. """
        if text == '\n':
            buff.handler_block(self._on_insert_text_handler_id)
            self._wml_interpreter.run_command(self.command_text)
            buff.insert_at_cursor("\n")
            self._insert_prompt()
            buff.handler_unblock(self._on_insert_text_handler_id)
            buff.emit_stop_by_name("insert-text")
