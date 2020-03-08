""""""
import re

from gi.repository.Gtk import ResponseType

from core.object_factory import ObjectFactory


class CreateObjectDialog():
    # TODO:
    # Add signals during __init__
    # Make children widget naming consistent
    # Make CreateObjectDialog a subclass of Gtk.Dialog

    def __init__(self, builder):
        self.dialog = builder.get_object("create_object_dialog")
        self.name_field = builder.get_object("name_dialog_field")
        self.POINTS_PATTERN = re.compile(r"^(-?\d+,-?\d+;)*-?\d+,-?\d+$")
        self.points_field = builder.get_object("wireframe_expression")
        self.handlers = {
            "on_create_object_ok": self._ok,
            "on_create_object_cancel": self._cancel,
        }

    def _cancel(self, _):
        """ Cancels dialog without creating object. """
        self.create_object_dialog.dialog.response(ResponseType.CANCEL)

    def clear(self):
        self.name_field.set_text("")
        self.points_field.set_text("")

    def handlers(self):
        return self.handlers

    def hide(self):
        self.dialog.hide()

    def name(self):
        return self.name_field.get_text()

    def _ok(self, _):
        """ Check if form input is valid. If so, create new object with it. """
        try:
            self.validate()
            ObjectFactory.make_object(self.name(), self.points())
            # Add object to TreeStore and make it visible
            self.dialog.response(ResponseType.OK)
        except RuntimeError as error:
            # Log error
            print(error)

    def points(self):
        return [
            (int(point[0]), int(point[1]))
            for point in map(lambda p: p.split(","),
            self.points_field.get_text().split(";"))]

    def run(self):
        return self.dialog.run()

    def validate(self):
        name = self.name()
        if name == "asd":
            raise RuntimeError("Name '" + name + "' already names an object!")

        points_expression = self.points_field.get_text()
        if not self.POINTS_PATTERN.match(points_expression):
            raise RuntimeError("Invalid list of points format!")
        # Smooth points?
