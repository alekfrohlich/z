""" Gtk client uses Builder with Glade to generate a GUI. """

import gi
gi.require_version('Gtk', '3.0')
from gi.repository.Gtk import main_iteration_do
from gi.repository.Gtk import Builder

from objects.window import Window

from client.window_manager import WindowManager
from client.gtk.object_store import GtkObjectStore

from client.gtk.gui.console import Console
from client.gtk.gui.menu_bar import MenuBar, CreateObjectDialog
from client.gtk.gui.control_menu import ControlMenu
from client.gtk.gui.viewport import ViewPort

from wml import WML_Interpreter


class GtkClient:
    def __init__(self):
        self._has_quit = False
        self._builder = Builder()
        self._builder.add_from_file("client/gtk/glade/z_gui_layout.glade")

        # Glade
        drawing_area = self._builder.get_object("viewport_drawing_area")
        # @FIXME: store -> obj_name_store to avoid confusion with ObjectStore
        store = self._builder.get_object("object_list_store")
        treeview = self._builder.get_object("object_list")
        window = Window()
        window_manager = WindowManager(window)
        display_file = {"window" : window}
        store.append([window.name, str(window.type)])

        # Need something
        viewport = ViewPort(drawing_area, window_manager, display_file)
        obj_store = GtkObjectStore(display_file, store, treeview, viewport, window_manager)
        wml_interpreter = WML_Interpreter(obj_store, viewport, display_file)
        console = Console(self._builder.get_object("console_text_view"), wml_interpreter)

        create_obj_dialog = CreateObjectDialog(
            self._builder.get_object("create_object_dialog"),
            self._builder.get_object("create_object_dialog_name_field"),
            self._builder.get_object("create_object_dialog_points_field"),
            self._builder.get_object("create_object_dialog_color_field"),
            obj_store,
            wml_interpreter)
        menu_bar = MenuBar(create_obj_dialog, obj_store)

        control_menu = ControlMenu(obj_store,
                                self._builder.get_object("degrees_entry"),
                                self._builder.get_object("point_entry"),
                                self._builder.get_object("step_entry"),
                                self._builder.get_object("center_of_world_radio_button"))

        # Handlers
        handlers = {
            "on_delete_event": lambda _, __: self.quit(),
            # Menu bar
            "on_menu_bar_quit": lambda _: self.quit(),
        }
        handlers.update(create_obj_dialog.handlers)
        handlers.update(control_menu.handlers)
        handlers.update(menu_bar.handlers)
        handlers.update(viewport.handlers)
        self._builder.connect_signals(handlers)

    def quit(self):
        self._has_quit = True

    def run(self):
        self._builder.get_object("main_window").show_all()
        while not self._has_quit:
            main_iteration_do(False)
