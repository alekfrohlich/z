""""""

class Console:
    def __init__(self, text_view, _wml_interpreter):
        self._text_view = text_view
        self._text_buffer = self._text_view.get_buffer()
        self._wml_interpreter = _wml_interpreter
        self._mark = self._text_buffer.create_mark("protected",
                                                   self._text_buffer
                                                   .get_end_iter())
        self._on_insert_text_handler_id = self._text_buffer.connect(
            "insert-text", self._on_insert_text)
        self._begin_command_mark = self._text_buffer.create_mark(
            "begin_command",
            self._text_buffer.get_start_iter(),
            True)
        self._unaccessible_tag = self._text_buffer.create_tag("unaccessible_tag", editable=False, editable_set=True)
        self._insert_prompt()

    # Attributes

    @property
    def command_text(self):
        """ String representation of the last typed command. """
        return self._text_buffer.get_text(self._text_buffer.get_iter_at_mark(self._begin_command_mark), self._text_buffer.get_end_iter(), False)

    def _insert_prompt(self):
        """"""
        self._text_buffer.insert_at_cursor(">> ")
        self._text_buffer.apply_tag(self._unaccessible_tag,
            self._text_buffer.get_start_iter(),
            self._text_buffer.get_end_iter())
        self._text_buffer.move_mark(self._begin_command_mark,
            self._text_buffer.get_end_iter())

    # Gtk signal handlers

    def _on_insert_text(self, buff, location, text, length):
        """ Run command based on the last typed line. """
        if text == '\n':
            buff.handler_block(self._on_insert_text_handler_id)
            self._wml_interpreter.run_command(self.command_text)
            buff.insert_at_cursor("\n")
            self._insert_prompt()
            buff.handler_unblock(self._on_insert_text_handler_id)
            buff.emit_stop_by_name("insert-text")
