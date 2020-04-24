"""This module provides graphical interface to object manipulation.

Classes
-------
    ControlMenu

"""
from enum import Enum

from gi.repository import Gtk

import numpy as np


class Axis(Enum):
    """Enum representing 3D Axis."""

    X = 0
    Y = 1
    Z = 2


class Direction(Enum):
    """Enum representing 2D directions."""

    IN = (0, 0, 1)
    OUT = (0, 0, -1)
    UP = (0, 1, 0)
    LEFT = (-1, 0, 0)
    RIGHT = (1, 0, 0)
    DOWN = (0, -1, 0)


class ControlMenu:
    """Control menu class.

    Handle move, zoom and rotate buttons. Acts upon selected object.

    Notes
    -----
        This GUI Component handles the following signals:

        - on_up_button : Gtk.Button.signals.clicked
        - on_left_button : Gtk.Button.signals.clicked
        - on_right_button : Gtk.Button.signals.clicked
        - on_down_button : Gtk.Button.signals.clicked
        - on_plus_button : Gtk.Button.signals.clicked
        - on_minus_button : Gtk.Button.signals.clicked
        - on_x_button : Gtk.Button.signals.clicked
        - on_y_button : Gtk.Button.signals.clicked
        - on_z_button : Gtk.Button.signals.clicked

    """

    def __init__(self, executor: 'Executor', obj_view: 'ObjectView',
                 degrees_entry: 'Gtk.Entry', point_entry: 'Gtk.Entry',
                 step_entry: 'Gtk.Entry', rotation_radio: 'Gtk.RadioButton'):
        """ControlMenu constructor."""
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
            "on_out_button": lambda _: self._on_translate(Direction.OUT),
            "on_in_button": lambda _: self._on_translate(Direction.IN),
            "on_plus_button": lambda _: self._on_scale(expand=True),
            "on_minus_button": lambda _: self._on_scale(expand=False),
            "on_x_button": lambda _: self._on_rotate(axis=Axis.X),
            "on_y_button": lambda _: self._on_rotate(axis=Axis.Y),
            "on_z_button": lambda _: self._on_rotate(axis=Axis.Z),
        }

    @property
    def degrees(self) -> 'float':
        """Rotation angle."""
        return float(self._degrees_entry.get_text())

    @property
    def point(self) -> 'tuple':
        """Rotation reference point."""
        p = self._point_entry.get_text().split(",")
        return (float(p[0]), float(p[1]), float(p[2]))

    @property
    def step(self) -> 'int':
        """Move/zoom step/factor."""
        return int(self._step_entry.get_text())

    @property
    def rotation_strategy(self) -> 'str':
        """Rotate around world, object or point."""
        group = self._rotation_radio.get_group()
        for radio in group:
            if radio.get_active():
                return radio.get_name()

    def _on_translate(self, direction: 'Direction'):
        """Handle on_{up,left,right,down}_button signals."""
        if self._obj_view.selected_object is not None:
            dx, dy, dz = direction.value
            self._executor.translate(
                self._obj_view.selected_object,
                dx * self.step,
                dy * self.step,
                dz * self.step)

    def _on_scale(self, expand: 'bool'):
        """Handle on_{plus,minus}_button signals."""
        if self._obj_view.selected_object is not None:
            factor = (1 + self.step/100) ** (1 if expand else -1)
            self._executor.scale(self._obj_view.selected_object, factor)

    def _on_rotate(self, axis: 'Axis'):
        """Handle on_{x,y,z}_button signals."""
        selected = self._obj_view.selected_object
        if selected is not None:
            rads = np.deg2rad(self.degrees)
            angles = [0, 0, 0]
            angles[axis.value] = rads
            if self.rotation_strategy == "world":
                self._executor.rotate(selected, *angles, (0, 0, 0))
            elif self.rotation_strategy == "object":
                self._executor.rotate(selected, *angles, None)
            else:
                self._executor.rotate(selected, *angles, self.point)
