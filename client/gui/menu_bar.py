"""This module provides dialogs for user actions initiated at the MenuBar.

Classes
-------
    MenuBar
    CreateObjectDialog

"""
from gi.repository import Gtk

from util import (Logger, LogLevel)
from client.objects import ObjectType


class MenuBar:
    """Menu bar class.

    Responsible for running and hiding dialogs. Successful dialog runs
    carry some action for the Executor to execute, e.g., creating a
    new object after CreateObjectDialogs returns 'OK'.

    """

    def __init__(self, create_obj_dialog: 'CreateObjectDialog',
                 load_obj_dialog: 'Gtk.FileChooserDialog',
                 executor: 'Executor', dot_obj_parser: 'DotObjParser'):
        """MenuBar constructor."""
        self._create_obj_dialog = create_obj_dialog
        self._load_obj_dialog = load_obj_dialog
        self._executor = executor
        self._dot_obj_parser = dot_obj_parser
        self.handlers = {
            "on_create_object": self._on_create_object,
            "on_load_object": self._on_load_object,
        }

    def _on_create_object(self, _):
        """Handle on_create_object signal.

        Run create_obj_dialog. Create object and hide dialog if it
        ran successfully.

        """
        response = self._create_obj_dialog.run()

        if response == Gtk.ResponseType.OK:
            str2type = {
                "Face element": None,
                "Bezier": ObjectType.BEZIER,
                "B-Spline": ObjectType.BSPLINE,
            }
            self._executor.add(self._create_obj_dialog.name,
                                self._create_obj_dialog.points,
                                self._create_obj_dialog.color,
                                str2type[self._create_obj_dialog.object_type])
        self._create_obj_dialog.hide()

    def _on_load_object(self, _):
        """Handle on_load_object signal.

        Run load_obj_dialog. Create object and hide dialog if it
        ran successfully.

        """
        response = self._load_obj_dialog.run()
        if response == Gtk.ResponseType.OK:
            self._dot_obj_parser.compile_obj_file(
                self._load_obj_dialog.get_filename())
        self._load_obj_dialog.hide()


class CreateObjectDialog:
    """Modal dialog for creating objects.

    CreateObjectDialog allows specifying the name, points and color
    of the future object.

    Notes
    -----
        CreateObjectDialog is dependency injected by Gtk.Builder during
        GtkClient construction.

        This GUI Component handles the following signals:

        - on_create_object_ok : Gtk.Button.signals.clicked
        - on_create_object_cancel : Gtk.Button.signals.clicked

    """

    def __init__(self, dialog: 'Gtk.Dialog', name_field: 'Gtk.Entry',
                 type_field: 'Gtk.ComboBoxText', points_field: 'Gtk.Entry',
                 color_field: 'Gtk.Entry', obj_view: 'ObjectView',
                 interpreter: 'Interpreter'):
        """CreateObjectDialog constructor."""
        self._dialog = dialog
        self._name_field = name_field
        self._type_field = type_field
        self._points_field = points_field
        self._color_field = color_field
        self._obj_view = obj_view
        self._wml_interpreter = interpreter
        self.handlers = {
            "on_create_object_ok": self._on_ok,
            "on_create_object_cancel": self._on_cancel,
        }

    @property
    def name(self) -> 'str':
        """Object's name."""
        return self._name_field.get_text()

    @property
    def object_type(self) -> 'str':
        # NOTE: already in face/curve/surface classification.
        """Object's type."""
        return self._type_field.get_active_text()

    @property
    def points(self) -> 'list':
        """Object's points."""
        return self._wml_interpreter.points_as_list(
            self._points_field.get_text())

    @property
    def color(self) -> 'tuple':
        """Object's color."""
        return self._wml_interpreter.color_as_tuple(
            self._color_field.get_text())

    def hide(self):
        """Gtk.Dialog.hide wrapper."""
        self._dialog.hide()

    def run(self):
        """Gtk.Dialog.run wrapper that automatically fills object name."""
        self._name_field.set_text("object{}".format(len(self._obj_view)))
        return self._dialog.run()

    def _on_cancel(self, _):
        """Handle on_create_object_cancel signal.

        Forces dialog to quit with cancel response type.

        """
        self._dialog.response(Gtk.ResponseType.CANCEL)

    def _on_ok(self, _):
        """Handle on_create_object_ok signal.

        Create object and return dialog if typed information is valid,
        else repeat form.

        Raises
        ------
            RuntimeError
                If the object is not valid.

        """
        try:
            self._wml_interpreter.validate_object(
                self.name, self._points_field.get_text())
            self._dialog.response(Gtk.ResponseType.OK)
        except RuntimeError as error:
            Logger.log(LogLevel.ERRO, error)
