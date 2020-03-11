""""""

import re

from gi.repository.Gtk import ResponseType

from core.log import Logger, LogLevel
from models.world import World
from wml import parse_points, POINTS_PATTERN


class CreateObjectDialog():

    def __init__(self, builder, list_store):
        self._dialog = builder.get_object("create_object_dialog")
        self._name_field = builder.get_object(
            "create_object_dialog_name_field")
        self._points_field = builder.get_object(
            "create_object_dialog_points_field")
        self.handlers = {
            "on_create_object_ok": self._on_ok,
            "on_create_object_cancel": self._on_cancel,
        }
        self._store = list_store

    @property
    def name(self):
        """ Name of the object. """
        return self._name_field.get_text()

    @property
    def points(self):
        """ List of points already cleaned. """
        return parse_points(self._points_field.get_text())

    def validate(self):
        """ Throw RuntimeError if either list of points is badly formatted or
            the chosen name is already in use. """
        for row in self._store:
            if row[0] == self.name:
                raise RuntimeError(self.name + "' already names an object!")

        exp = self._points_field.get_text()
        if not POINTS_PATTERN.match(exp):
            raise RuntimeError("Invalid list of points format!")

    # Gtk.Dialog wrappers

    def hide(self):
        """ dialog.hide wrapper. """
        self._dialog.hide()

    def run(self):
        """ dialog.run wrapper that automatically updates the name field. """
        self._name_field.set_text("object{}".format(World.size()))
        return self._dialog.run()

    # Gtk signal handlers

    def _on_cancel(self, _):
        """ Cancels dialog without creating object. """
        self._dialog.response(ResponseType.CANCEL)

    def _on_ok(self, _):
        """ Check if form input is valid. If so, create new object with it. """
        try:
            self.validate()
            self._dialog.response(ResponseType.OK)
        except RuntimeError as error:
            Logger.log(LogLevel.ERROR, error)
