""""""
""""""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository.Gtk import main_iteration_do
from gi.repository.Gtk import Builder

from .executor import GtkExecutor
from .object_store import ObjectStore

from .gui import (Console, ControlMenu, MenuBar, CreateObjectDialog, ObjectView, Viewport)

from wml import Interpreter


class GtkClient:
    def __init__(self):
        self._has_quit = False
        self._builder = Builder()
        self._builder.add_from_file("glade/gtk_client.glade")

        obj_store = ObjectStore()
        obj_view = ObjectView(
            obj_store, self._builder.get_object("object_list"))

        viewport = Viewport(
            self._builder.get_object("viewport_drawing_area"), obj_store)

        executor = GtkExecutor(obj_store, viewport)

        interpreter = Interpreter(executor)

        Console(self._builder.get_object("console_text_view"), interpreter)

        create_obj_dialog = CreateObjectDialog(
            self._builder.get_object("create_object_dialog"),
            self._builder.get_object("create_object_dialog_name_field"),
            self._builder.get_object("create_object_dialog_points_field"),
            self._builder.get_object("create_object_dialog_color_field"),
            obj_view,
            interpreter)
        menu_bar = MenuBar(create_obj_dialog, executor)

        control_menu = ControlMenu(executor,
                                   obj_view,
                                   self._builder.get_object("degrees_entry"),
                                   self._builder.get_object("point_entry"),
                                   self._builder.get_object("step_entry"),
                                   self._builder.get_object(
                                       "center_of_world_radio_button"))

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
