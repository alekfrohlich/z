"""Package containing initialization code for the GTK z-client.

The GTK client's layout is composed of

- console: A console with an embedded interpreter.
- control_menu: A control menu for manipulating the selected object.
- menu_bar: A menu bar with the following options:
    * Create Object (Shift+4)
- object_view: A scrolling window for displaying information about
  existing objects and for selecting one them.
- viewport: A viewport for visualizing a part of the 2D world.

Components that need to create/remove/manipulate objects do so by
interacting with the executor interface. Viewport is an exception
as it performs read only access to the list of objects (it draws them).

Notes
-----
    The graphical user interface is maintained using Glade, a RAD tool for
    building Gtk+ based GUI's and loaded using the Gtk.Builder class.

"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .executor import Executor
from .object_store import ObjectStore

from .gui import *

from util import DotObjParser
from wml import Interpreter


class GtkClient:
    def __init__(self):
        """Initialize gtk client.

        Constructs GUI from glade file and realizes dependency injections.

        """
        self._has_quit = False
        self._builder = Gtk.Builder()
        self._builder.add_from_file("glade/gtk_client.glade")

        obj_store = ObjectStore()
        obj_view = ObjectView(
            obj_store, self._builder.get_object("object_list"))

        viewport = Viewport(
            self._builder.get_object("viewport_drawing_area"), obj_store)

        executor = Executor(obj_store, viewport)
        dot_obj_parser = DotObjParser(executor)

        interpreter = Interpreter(executor)

        Console(self._builder.get_object("console_text_view"), interpreter)

        create_obj_dialog = CreateObjectDialog(
            self._builder.get_object("create_object_dialog"),
            self._builder.get_object("create_object_dialog_name_field"),
            self._builder.get_object("create_object_dialog_points_field"),
            self._builder.get_object("create_object_dialog_color_field"),
            obj_view,
            interpreter)
        load_obj_dialog = Gtk.FileChooserDialog(
            "Please choose a .obj file",
            self._builder.get_object("main_window"),  # Modal for
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL,
             Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        menu_bar = MenuBar(
            create_obj_dialog, load_obj_dialog, executor, dot_obj_parser)

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
        """Indicate that the user has quit."""
        self._has_quit = True

    def run(self):
        """Process Gtk events until `quit()` is called."""
        self._builder.get_object("main_window").show_all()
        while not self._has_quit:
            Gtk.main_iteration_do(False)
