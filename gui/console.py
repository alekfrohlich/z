""""""

from wml import parse_points, ADD_PATTERN
from models.world import World

# TODO: add new line repl (solve invalid TextIter)


class Console:
    def __init__(self, store, text_view):
        self._store = store
        self._text_view = text_view
        self._text_buffer = self._text_view.get_buffer()
        self._mark = self._text_buffer.create_mark("protected",
                                                   self._text_buffer
                                                   .get_end_iter())
        self.handlers = {
            "on_insert_text": self._on_insert_text,
        }

    def run_command(self, string):
        # FIXME: match other commands and behave properly
        match = ADD_PATTERN.match(string)
        if match:
            add_expression = match.group()
            points = parse_points(add_expression[4:len(add_expression)-2])

            obj = World.make_object("", points)
            self._store.append([obj.name, str(obj.type)])

    # Gtk signal handlers

    def _on_insert_text(self, buff, location, text, length):
        """ Run command based on the last typed line. """
        if text == '\n':
            self.run_command(buff.get_text(buff.get_start_iter(),
                                           buff.get_end_iter(), True))
