""" Dialogs started by doing some action in the MainWindow. """

from gi.repository.Gtk import ResponseType

from util.log import Logger, LogLevel


class CreateObjectDialog():
    def __init__(self, dialog, name_field, points_field, color_field,
                 object_factory, wml_interpreter):
        self._dialog = dialog
        self._name_field = name_field
        self._points_field = points_field
        self._color_field = color_field
        self._object_factory = object_factory
        self._wml_interpreter = wml_interpreter
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
        return self._wml_interpreter.points_as_list(
            self._points_field.get_text())

    @property
    def color(self):
        """ Color of the object. """
        return self._wml_interpreter.color_as_tuple(
            self._color_field.get_text())

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
            self._wml_interpreter.validate_object(
                self.name, self._points_field.get_text())
            self._dialog.response(ResponseType.OK)
        except RuntimeError as error:
            Logger.log(LogLevel.ERROR, error)
