""""""

import re

from gi.repository.Gtk import ResponseType

from core.log import Logger, LogLevel\


class CreateObjectDialog():
    # TODO:
    # Add signals during __init__
    # Make children widget naming consistent
    # Make CreateObjectDialog a subclass of Gtk.Dialog

    POINTS_PATTERN = re.compile(r"^(-?\d+,-?\d+;)*-?\d+,-?\d+$")

    def __init__(self, builder, list_store):
        self._dialog = builder.get_object("create_object_dialog")
        self._name_field = builder.get_object("name_dialog_field")
        self._points_field = builder.get_object("wireframe_expression")
        self.handlers = {
            "on_create_object_ok": self._on_ok,
            "on_create_object_cancel": self._on_cancel,
        }
        self._store = list_store

    def _on_cancel(self, _):
        """ Cancels dialog without creating object. """
        self._dialog.response(ResponseType.CANCEL)

    # def clear(self):
    #     self._name_field.set_text("")
    #     self._points_field.set_text("")

    def hide(self):
        self._dialog.hide()

    @property
    def name(self):
        return self._name_field.get_text()

    def _on_ok(self, _):
        """ Check if form input is valid. If so, create new object with it. """
        try:
            self.validate()
            self._dialog.response(ResponseType.OK)
        except RuntimeError as error:
            Logger.log(LogLevel.ERROR, error)

    @property
    def points(self):
        return [
            (int(point[0]), int(point[1]))
            for point in map(lambda p: p.split(","),
            self._points_field.get_text().split(";"))]

    def run(self):
        return self._dialog.run()

    def validate(self):
        for row in self._store:
            if row[0] == self.name:
                raise RuntimeError("Name '" + self.name + "' already names an object!")

        exp = self._points_field.get_text()
        if not CreateObjectDialog.POINTS_PATTERN.match(exp):
            raise RuntimeError("Invalid list of points format!")
        # Smooth points?
