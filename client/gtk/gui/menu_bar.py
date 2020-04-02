""" """

from gi.repository.Gtk import ResponseType

from util.log import Logger, LogLevel


class MenuBar:
    def __init__(self, create_obj_dialog, executor):
        self._create_obj_dialog = create_obj_dialog
        self._executor = executor
        self.handlers = {
            "on_create_object": self._on_create_object,
        }

    def _on_create_object(self, _):
        response = self._create_obj_dialog.run()

        if response == ResponseType.OK:
            self._executor.add(self._create_obj_dialog.name,
                               self._create_obj_dialog.points,
                               self._create_obj_dialog.color)
        self._create_obj_dialog.hide()


class CreateObjectDialog:
    def __init__(self, dialog, name_field, points_field, color_field,
                 obj_store, wml_interpreter):
        self._dialog = dialog
        self._name_field = name_field
        self._points_field = points_field
        self._color_field = color_field
        self._obj_store = obj_store
        self._wml_interpreter = wml_interpreter
        self.handlers = {
            "on_create_object_ok": self._on_ok,
            "on_create_object_cancel": self._on_cancel,
        }

    @property
    def name(self):
        return self._name_field.get_text()

    @property
    def points(self):
        return self._wml_interpreter.points_as_list(
            self._points_field.get_text())

    @property
    def color(self):
        return self._wml_interpreter.color_as_tuple(
            self._color_field.get_text())

    # Gtk.Dialog wrappers

    def hide(self):
        self._dialog.hide()

    def run(self):
        self._name_field.set_text(self._obj_store.next_available_name)
        return self._dialog.run()

    # Gtk signal handlers

    def _on_cancel(self, _):
        self._dialog.response(ResponseType.CANCEL)

    def _on_ok(self, _):
        try:
            self._wml_interpreter.validate_object(
                self.name, self._points_field.get_text())
            self._dialog.response(ResponseType.OK)
        except RuntimeError as error:
            Logger.log(LogLevel.ERROR, error)
