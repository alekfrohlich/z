""""""

from gi.repository.Gtk import TextTag

from wml import run_command
from models.world import World

# TODO: add new line repl

class Console:
    def __init__(self, text_view, store):
        self._text_view = text_view
        self._text_buffer = self._text_view.get_buffer()
        self._store = store
        self.handlers = {
            "on_insert_text": self._on_insert_text,
        }

    # Gtk signal handlers

    def _on_insert_text(self, buff, location, text, length):
        if text is '\n':
            self.run_command(buff.get_text())
            buff.set_text(">> ")
