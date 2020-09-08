"""This module provides dialogs for user actions initiated at the MenuBar.

Classes
-------
    MenuBar
    CreateObjectDialog

"""
from gi.repository import Gtk

from client.models.curve import Interpolator
from util import (Logger, LogLevel)


class MenuBar:
    """Menu bar class.

    Responsible for running dialogs from the GUI.

    Structure:

    - File
      - Load .obj file
      - Export selection as .obj file
      - Load .oml file
    -------------------
      - Quit (CTRL+Q)

    - Create
      - New Object (SHIFT+4)

    - Help (Not implemented)

    """

    def __init__(self, create_obj_dialog: 'CreateObjectDialog',
                 file_chooser_dialog: 'Gtk.FileChooserDialog',
                 file_saver_dialog: 'Gtk.FileChooserDialog',
                 executor: 'Executor', dot_obj_parser: 'DotObjParser',
                 dot_oml_parser: 'DotOmlParser', obj_view: 'ObjectView'):
        """MenuBar constructor."""
        self._create_obj_dialog = create_obj_dialog
        self._file_chooser_dialog = file_chooser_dialog
        self._file_saver_dialog = file_saver_dialog
        self._executor = executor
        self._dot_obj_parser = dot_obj_parser
        self._dot_oml_parser = dot_oml_parser
        self._obj_view = obj_view
        self.handlers = {
            "on_create_object": self._on_create_object,
            "on_export_object" : self._on_export_object,
            "on_load_object": self._on_load_object,
            "on_run_script": self._on_run_script,
        }

    def _on_create_object(self, _):
        """Handle on_create_object signal.

        Run create_obj_dialog, and create object if the dialog ran
        successfully.

        """
        response = self._create_obj_dialog.run()

        if response == Gtk.ResponseType.OK:
            obj_type = self._create_obj_dialog.object_type
            params = {
                'name': self._create_obj_dialog.name,
                'points': self._create_obj_dialog.points,
                'color': self._create_obj_dialog.color,
                'obj_type': obj_type,
            }

            if obj_type == "Wireframe":
                # NOTE: Interpreting all points as a single face
                params['faces'] = [list(range(len(params['points'])))]
            elif obj_type == "Curve":
                # TODO: Add bmatu
                params['bmatu'] = Interpolator.BEZIER
            elif obj_type == "Surface":
                # TODO: Add bmatv
                params['bmatu'] = Interpolator.BEZIER
                params['bmatv'] = Interpolator.BEZIER

            self._executor.add(**params)

        self._create_obj_dialog.hide()

    def _on_export_object(self, _):
        """Handle on_export_object signal.

        # Run file_saver_dialog, and save selected object as .obj if
        # the dialog ran successfully.

        """
        response = self._file_saver_dialog.run()
        if response == Gtk.ResponseType.OK:
            self._dot_obj_parser.export_obj_file(
                self._file_saver_dialog.get_filename(),
                self._executor.get(self._obj_view.selected_object))
        self._file_saver_dialog.hide()

    def _on_load_object(self, _):
        """Handle on_load_object signal.

        Run file_chooser_dialog, and interpret selected file as .obj if
        the dialog ran successfully.

        """
        response = self._file_chooser_dialog.run()
        if response == Gtk.ResponseType.OK:
            self._dot_obj_parser.compile_obj_file(
                self._file_chooser_dialog.get_filename())
        self._file_chooser_dialog.hide()

    def _on_run_script(self, _):
        """Handle on_run_script signal.

        Run file_chooser_dialog, and interpret selected file as .oml if
        the dialog ran successfully.

        """
        response = self._file_chooser_dialog.run()
        if response == Gtk.ResponseType.OK:
            self._dot_oml_parser.interpret_oml_file(
                self._file_chooser_dialog.get_filename())
        self._file_chooser_dialog.hide()


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
        """Name of the object."""
        return self._name_field.get_text()

    @property
    def object_type(self) -> 'str':
        """Type of the object."""
        return self._type_field.get_active_text()

    @property
    def points(self) -> 'list':
        """List of points of the object."""
        return self._wml_interpreter.points_as_list(
            self._points_field.get_text())

    @property
    def color(self) -> 'tuple':
        """Color of the object."""
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
