""" Dialogs started by doing some action in the MainWindow. """

from gi.repository.Gtk import ResponseType

from core.log import Logger, LogLevel
from wml import points_as_list, parse_points


class CreateObjectDialog():
    def __init__(self, dialog, name_field, points_field, list_store,
                 object_factory):
        self._dialog = dialog
        self._name_field = name_field
        self._points_field = points_field
        self._store = list_store
        self._object_factory = object_factory
        self.handlers = {
            "on_create_object_ok": self._on_ok,
            "on_create_object_cancel": self._on_cancel,
        }

    @property
    def name(self):
        """ Name of the object. """
        return self._name_field.get_text()

    @property
    def points(self):
        """ List of points already cleaned. """
        return points_as_list(self._points_field.get_text())

    def validate(self):
        """ Throw RuntimeError if either list of points is badly formatted or
            the chosen name is already in use. """
        for row in self._store:
            if row[0] == self.name:
                raise RuntimeError(self.name + "' already names an object!")

        if not parse_points(self._points_field.get_text()):
            raise RuntimeError("Invalid list of points format!")

    # Gtk.Dialog wrappers

    def hide(self):
        """ dialog.hide wrapper. """
        self._dialog.hide()

    def run(self):
        """ dialog.run wrapper that automatically updates the name field. """
        self._name_field.set_text(self._object_factory.default_object_name())
        return self._dialog.run()

    # Gtk signal handlers

    def _on_cancel(self, _):
        """ Cancels dialog. """
        self._dialog.response(ResponseType.CANCEL)

    def _on_ok(self, _):
        """ Check if form input is valid. If so, returns OK, else logs
            error. """
        try:
            self.validate()
            self._dialog.response(ResponseType.OK)
        except RuntimeError as error:
            Logger.log(LogLevel.ERROR, error)
