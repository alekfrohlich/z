""" Main application window. """

from gi.repository.Gtk import ResponseType

import numpy as np

from util import AxisType, DirectionType

class ControlMenu:
    def __init__(self, executor, obj_view, degrees_entry, point_entry, step_entry,
                 rotation_radio):
        self._executor = executor
        self._obj_view = obj_view

        self._degrees_entry = degrees_entry
        self._point_entry = point_entry
        self._step_entry = step_entry
        self._rotation_radio = rotation_radio

        self.handlers = {
            "on_up_button": lambda _: self._on_translate(DirectionType.UP),
            "on_left_button": lambda _: self._on_translate(DirectionType.LEFT),
            "on_right_button": lambda _: self._on_translate(
                DirectionType.RIGHT),
            "on_down_button": lambda _: self._on_translate(DirectionType.DOWN),
            "on_plus_button": lambda _: self._on_scale(expand=True),
            "on_minus_button": lambda _: self._on_scale(expand=False),
            "on_x_button": lambda _: self._on_rotate(axis=AxisType.X),
            "on_y_button": lambda _: self._on_rotate(axis=AxisType.Y),
            "on_z_button": lambda _: self._on_rotate(axis=AxisType.Z),
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
    def rotation_strategy(self):
        """ Selects the active radio button from the rotation menu. """
        group = self._rotation_radio.get_group()
        for radio in group:
            if radio.get_active():
                return radio.get_name()

    # Gtk signal handlers

    def _on_translate(self, direction):
        """ Translate the selected object by the offset specified in the
            control menu. If there is no such object, translates the window
            instead. """
        if self._obj_view.selected_object is not None:
            dx, dy = direction.value
            self._executor.translate(self._obj_view.selected_object, dx * self.step, dy * self.step)

    def _on_scale(self, expand):
        """ Scales the selected object by the factor specified in the control
            menu. """
        if self._obj_view.selected_object is not None:
            factor = (1 + self.step/100) ** (1 if expand else -1)
            self._executor.scale(self._obj_view.selected_object, factor)

    def _on_rotate(self, axis):
        """ Rotates the selected object in respect to the given point
            by the amount specified in the control menu. """
        # axis is not used (yet!)
        selected = self._obj_view.selected_object
        if selected is not None:
            rads = np.deg2rad(self.degrees)
            if self.rotation_strategy == "world":
                self._executor.rotate(selected, rads, (0,0))
            elif self.rotation_strategy == "object":
                self._executor.rotate(selected, rads, None)
            else:
                self._executor.rotate(selected, rads, self.point)
