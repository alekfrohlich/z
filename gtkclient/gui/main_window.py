""" Main application window. """

from gi.repository.Gtk import ResponseType

import numpy as np

from core import AxisType, DirectionType
from gtkclient.gui.viewport import ViewPort


class MainWindow:
    def __init__(self, create_obj_dialog, obj_factory, treeview, viewport,
                 window, display_file, degrees_entry, point_entry, step_entry,
                 rotation_radio):
        self._create_object_dialog = create_obj_dialog
        self._obj_factory = obj_factory
        self._treeview = treeview
        self._viewport = viewport
        self._window = window
        self._display_file = display_file

        self._degrees_entry = degrees_entry
        self._point_entry = point_entry
        self._step_entry = step_entry

        self._rotation_radio = rotation_radio

        self.handlers = {
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
            # SHALL BE MOVED
            "on_create_object": self._on_create_object,
        }

    # Attributes

    @property
    def degrees(self):
        """ Degrees entry under rotation menu. Used for specifying the rotation
            amount. """
        return float(self._degrees_entry.get_text())

    @property
    def point(self):
        """ Point entry under the rotation menu. Used for specifying arbitrary
            reference of rotation. """
        p = self._point_entry.get_text().split(",")
        return (float(p[0]), float(p[1]))

    @property
    def step(self):
        """ Step entry under the window menu. Used for specifying the x-y
            offset/scale factor for translating/scaling objects and
            the window. """
        return int(self._step_entry.get_text())

    @property
    def selected_object(self):
        """ Currently selected object in TreeView. """
        tree_model, tree_iter = self._treeview.get_selection().get_selected()
        if tree_iter is not None:
            return self._display_file[tree_model.get_value(tree_iter, 0)]
        else:
            return None

    @property
    def rotation_strategy(self):
        """ Selects the active radio button from the rotation menu. """
        group = self._rotation_radio.get_group()
        for radio in group:
            if radio.get_active():
                return radio.get_name()

    # Gtk signal handlers

    @ViewPort.needs_redraw
    def _on_create_object(self, _):
        """ Show 'Create object' dialog and wait for it's response. If
            successful the display is hidden (not destroyed) and an object
            is created. """
        response = self._create_object_dialog.run()

        if response == ResponseType.OK:
            obj = self._obj_factory.make_object(self._create_object_dialog.name,
                                          self._create_object_dialog.points)
            obj.setColor(self._create_object_dialog.color)
        self._create_object_dialog.hide()

    @ViewPort.needs_redraw
    def _on_translate(self, direction):
        """ Translate the selected object by the offset specified in the
            control menu. If there is no such object, translates the window
            instead. """
        dx, dy = direction.value
        if self.selected_object is not None:
            self.selected_object.translate(dx * self.step, dy * self.step)
        else:
            self._window.translate(dx * self.step, dy * self.step)

    @ViewPort.needs_redraw
    def _on_scale(self, expand):
        """ Scales the selected object by the factor specified in the control
            menu. If there is no selected object, scales the window
            instead. """
        if self.selected_object is not None:
            factor = (1 + self.step/100) ** (1 if expand else -1)
            self.selected_object.scale(factor, factor)
        else:
            factor = (1 + self.step/100) ** (-1 if expand else 1)
            self._window.scale(factor, factor)

    @ViewPort.needs_redraw
    def _on_rotate(self, axis):
        # axis is not used (yet!)
        """ Rotates the selected object in respect to the given rotation
            strategy by the amount specified in the control menu. If there
            is no selected object, translates the window instead. """
        rads = np.deg2rad(self.degrees)
        if self.selected_object is not None:
            if self.rotation_strategy == "world":
                self.selected_object.rotate(rads, (0, 0))
            elif self.rotation_strategy == "object":
                self.selected_object.rotate(rads)
            else:
                self.selected_object.rotate(rads, self.point)
        else:
            self._window.rotate(rads)
