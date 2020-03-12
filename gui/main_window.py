""" Main application window (Gtk3 - Glade). """

from gi.repository.Gtk import main_quit
from gi.repository.Gtk import Builder
from gi.repository.Gtk import ResponseType

from core import DirectionType
from gui.console import Console
from gui.dialogs import CreateObjectDialog
from gui.viewport import ViewPort
from models.world import World
from models.window import Window


class MainWindow:
    """
        Main GUI window, has access to glade builder and thus is responsible
        for passing it around to other Glade-related graphical components.
    """

    def needs_redraw(f):
        """ Decorates methods that modify the display file and thus demand it
            to be redrawn to take effect. """
        def wrapper(self, *args, **kwargs):
            f(self, *args, **kwargs)
            self._builder.get_object("viewport").queue_draw()
        return wrapper

    def __init__(self):
        self._builder = Builder()
        self._builder.add_from_file("glade/z_gui_layout.glade")
        self._builder.get_object("viewport").set_size_request(
            *ViewPort.RESOLUTION)

        self._store = self._builder.get_object("object_list_store")
        self._treeview = self._builder.get_object("object_list")
        self._treeview.set_model(self._store)

        self._console = Console(self._store, self._builder.get_object(
                                "console_text_view"))
        self._create_object_dialog = CreateObjectDialog(
            self._builder.get_object("create_object_dialog"),
            self._builder.get_object("create_object_dialog_name_field"),
            self._builder.get_object("create_object_dialog_points_field"),
            self._store)
        self._viewport = ViewPort(self._builder)
        handlers = {
            "on_destroy": main_quit,
            # Controls
            "on_up_button": lambda _: self._on_translate(DirectionType.UP),
            "on_left_button": lambda _: self._on_translate(DirectionType.LEFT),
            "on_right_button": lambda _: self._on_translate(
                DirectionType.RIGHT),
            "on_down_button": lambda _: self._on_translate(DirectionType.DOWN),
            "on_zoom_in": lambda _: self._on_scale(expand=True),
            "on_zoom_out": lambda _: self._on_scale(expand=False),
            "on_x_button": self.fixme,
            "on_y_button": self.fixme,
            "on_z_button": self.fixme,
            # Menu bar
            "on_menu_bar_quit": main_quit,
            "on_create_object": self._on_create_object,
        }
        handlers.update(self._console.handlers)
        handlers.update(self._create_object_dialog.handlers)
        handlers.update(self._viewport.handlers)
        self._builder.connect_signals(handlers)

    def fixme(self, _):
        print("Feature not yet implemented!")

    def show(self):
        """ Display application window. """
        self._builder.get_object("main_window").show_all()

    # Attributes

    @property
    def step(self):
        """ x-y offset/scale factor for translating/scaling objects and/or
            the window. """
        return int(self._builder.get_object("step_entry").get_text())

    @property
    def selected_object(self):
        """ Currently selected object in TreeView. """
        tree_model, tree_iter = self._treeview.get_selection().get_selected()
        if tree_iter is not None:
            return World.objects()[tree_model.get_value(tree_iter, 0)]
        else:
            return None

    # Gtk signal handlers

    @needs_redraw
    def _on_create_object(self, _):
        """ Show 'Create object' dialog and wait for it's response. Note that
            if successful the display is hidden again (not destroyed). """
        response = self._create_object_dialog.run()

        if response == ResponseType.OK:
            obj = World.make_object(self._create_object_dialog.name,
                                    self._create_object_dialog.points)
            self._store.append([obj.name, str(obj.type)])
        self._create_object_dialog.hide()

    @needs_redraw
    def _on_translate(self, direction):
        """ Translate the selected object by the offset specified in the
            control menu. If there is no such object, translates the window
            instead. """
        dx, dy = direction.value
        if self.selected_object is not None:
            self.selected_object.translate(dx * self.step, dy * self.step)
        else:
            Window.translate(dx * self.step, dy * self.step)

    @needs_redraw
    def _on_scale(self, expand):
        """ Translate the selected object towards direction by the offset
            specified in the control menu. If there is no selected object,
            translates the window instead. """
        if self.selected_object is not None:
            factor = (1 + self.step/100) ** (1 if expand else -1)
            self.selected_object.scale(factor, factor)
        else:
            factor = (1 + self.step/100) ** (-1 if expand else 1)
            Window.scale(factor, factor)
