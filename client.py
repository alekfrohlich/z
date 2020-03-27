""" Gtk client uses Builder with Glade to generate a GUI. """

import gi
gi.require_version('Gtk', '3.0')
from gi.repository.Gtk import main_iteration_do
from gi.repository.Gtk import Builder

from gtkclient.object_factory import GtkObjectFactory
from gtkclient.gui.console import Console
from gtkclient.gui.dialogs import CreateObjectDialog
from gtkclient.gui.main_window import MainWindow
from gtkclient.gui.viewport import ViewPort

from objects.window import Window

from wml import WML_Interpreter


class Client:
    def __init__(self):
        self._has_quit = False
        self._builder = Builder()
        self._builder.add_from_file("gtkclient/glade/z_gui_layout.glade")

        # Dont need anything
        window = Window()
        display_file = {}

        # Glade
        drawing_area = self._builder.get_object("viewport_drawing_area")
        store = self._builder.get_object("object_list_store")
        treeview = self._builder.get_object("object_list")

        # Need something
        viewport = ViewPort(drawing_area, window, display_file)
        obj_factory = GtkObjectFactory(store, viewport, display_file)
        wml_interpreter = WML_Interpreter(obj_factory, viewport, display_file)
        console = Console(self._builder.get_object("console_text_view"), wml_interpreter)
        create_obj_dialog = CreateObjectDialog(
            self._builder.get_object("create_object_dialog"),
            self._builder.get_object("create_object_dialog_name_field"),
            self._builder.get_object("create_object_dialog_points_field"),
            self._builder.get_object("create_object_dialog_color_field"),
            obj_factory,
            wml_interpreter)
        main_window = MainWindow(create_obj_dialog, obj_factory, treeview,
                                viewport,
                                window,
                                display_file,
                                self._builder.get_object("degrees_entry"),
                                self._builder.get_object("point_entry"),
                                self._builder.get_object("step_entry"),
                                self._builder.get_object("center_of_world_radio_button"))

        # Handlers
        handlers = {
            "on_delete_event": self.quit,
            # Menu bar
            "on_menu_bar_quit": self.quit,
        }
        handlers.update(main_window.handlers)
        handlers.update(create_obj_dialog.handlers)
        handlers.update(viewport.handlers)
        self._builder.connect_signals(handlers)

    def quit(self, __=None, _=None):
        self._has_quit = True

    def run(self):
        self._builder.get_object("main_window").show_all()
        while not self._has_quit:
            main_iteration_do(False)
