""" Main application window. """

from gi.repository.Gtk import ResponseType

import numpy as np

from util import AxisType, DirectionType

class ControlMenu:
    def __init__(self, obj_store, degrees_entry, point_entry, step_entry,
                 rotation_radio):
        self._obj_store = obj_store

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
            # ON EXPAND, ON SHRINK
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
        """ Notifies ObjectStore that a translation happened. """
        dx, dy = direction.value
        self._obj_store.translate(dx * self.step, dy * self.step)

    def _on_scale(self, expand):
        """ Notifies ObjectStore that an escalation happened. """
        factor = (1 + self.step/100) ** (1 if expand else -1)
        self._obj_store.scale(factor)

    def _on_rotate(self, axis):
        """ Notifies ObjectStore that a rotation happened. """
        # axis is not used (yet!)
        rads = np.deg2rad(self.degrees)
        if self.rotation_strategy == "world":
            self._obj_store.rotate(rads, (0,0))
        elif self.rotation_strategy == "object":
            self._obj_store.rotate(rads, None)
        else:
            self._obj_store.rotate(rads, self.point)
