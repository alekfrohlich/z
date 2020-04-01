""" Main application window. """

import numpy as np

from util import Axis, Direction


class ControlMenu:
    def __init__(self, executor, obj_view, degrees_entry, point_entry,
                 step_entry, rotation_radio):
        self._executor = executor
        self._obj_view = obj_view

        self._degrees_entry = degrees_entry
        self._point_entry = point_entry
        self._step_entry = step_entry
        self._rotation_radio = rotation_radio

        self.handlers = {
            "on_up_button": lambda _: self._on_translate(Direction.UP),
            "on_left_button": lambda _: self._on_translate(Direction.LEFT),
            "on_right_button": lambda _: self._on_translate(Direction.RIGHT),
            "on_down_button": lambda _: self._on_translate(Direction.DOWN),
            "on_plus_button": lambda _: self._on_scale(expand=True),
            "on_minus_button": lambda _: self._on_scale(expand=False),
            "on_x_button": lambda _: self._on_rotate(axis=Axis.X),
            "on_y_button": lambda _: self._on_rotate(axis=Axis.Y),
            "on_z_button": lambda _: self._on_rotate(axis=Axis.Z),
        }

    # Attributes

    @property
    def degrees(self):
        return float(self._degrees_entry.get_text())

    @property
    def point(self):
        p = self._point_entry.get_text().split(",")
        return (float(p[0]), float(p[1]))

    @property
    def step(self):
        return int(self._step_entry.get_text())

    @property
    def rotation_strategy(self):
        group = self._rotation_radio.get_group()
        for radio in group:
            if radio.get_active():
                return radio.get_name()

    # Gtk signal handlers

    def _on_translate(self, direction):
        if self._obj_view.selected_object is not None:
            dx, dy = direction.value
            self._executor.translate(
                self._obj_view.selected_object, dx * self.step, dy * self.step)

    def _on_scale(self, expand):
        if self._obj_view.selected_object is not None:
            factor = (1 + self.step/100) ** (1 if expand else -1)
            self._executor.scale(self._obj_view.selected_object, factor)

    def _on_rotate(self, axis):
        # axis is not used (yet!)
        selected = self._obj_view.selected_object
        if selected is not None:
            rads = np.deg2rad(self.degrees)
            if self.rotation_strategy == "world":
                self._executor.rotate(selected, rads, (0, 0))
            elif self.rotation_strategy == "object":
                self._executor.rotate(selected, rads, None)
            else:
                self._executor.rotate(selected, rads, self.point)
