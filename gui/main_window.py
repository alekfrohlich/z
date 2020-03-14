""" Main application window (Gtk3 - Glade). """

from gi.repository.Gtk import main_quit
from gi.repository.Gtk import Builder
from gi.repository.Gtk import ResponseType

import numpy as np

from core import AxisType, DirectionType
from gui.console import Console
from gui.dialogs import CreateObjectDialog
from gui.viewport import ViewPort
from models.world import World
from models.window import Window
from wml import WML_Interpreter


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

        self._console = Console(self._builder.get_object("console_text_view"),
                                WML_Interpreter(self._store))
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
            "on_x_button": lambda _: self._on_rotate(axis=AxisType.X),
            "on_y_button": lambda _: self._on_rotate(axis=AxisType.Y),
            "on_z_button": lambda _: self._on_rotate(axis=AxisType.Z),
            # Menu bar
            "on_menu_bar_quit": main_quit,
            "on_create_object": self._on_create_object,
        }
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
    def degrees(self):
        """"""
        return float(self._builder.get_object("degrees_entry").get_text())

    @property
    def point(self):
        """"""
        return int(self._builder.get_object("point_entry").get_text())

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

    @property
    def rotation_strategy(self):
        group = self._builder.get_object(
            "center_of_world_radio_button").get_group()
        for radio in group:
            if radio.get_active():
                return radio.get_name()

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

    @needs_redraw
    def _on_rotate(self, axis):
        """"""
        rads = np.deg2rad(self.degrees)
        if self.selected_object is not None:
            if self.rotation_strategy == "world":
                self.selected_object.rotate(rads, (0, 0))
            elif self.rotation_strategy == "object":
                self.selected_object.rotate(rads)
            else:
                # FIXME: parse point into tuple of ints
                self.selected_object.rotate(rads, self.point_entry)
        else:
            Window.rotate(self.degrees)
