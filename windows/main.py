""""""

from gi.repository import Gtk

class MainWindow:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("glade/z_gui_layout.glade")
        self.builder.get_object("viewport").set_size_request(500,500)
        handlers = {
            "on_destroy" : Gtk.main_quit,
            "on_draw": self.fixme,
            # Controls
            "on_up_button": self.fixme,
            "on_left_button":  self.fixme,
            "on_right_button": self.fixme,
            "on_down_button":  self.fixme,
            "on_zoom_in":  self.fixme,
            "on_zoom_out": self.fixme,
            "on_x_button": self.fixme,
            "on_y_button": self.fixme,
            "on_z_button": self.fixme,
            # Menu bar
            "on_menu_bar_quit": Gtk.main_quit,
            "on_create_object": self._create_object,
            # Create object dialog
            "on_create_object_ok": self._dialog_ok,
            "on_create_object_cancel": self._dialog_close,

        }
        self.builder.connect_signals(handlers)
        self.dialog = None

    def fixme(self, _):
        print("Feature not yet implemented!")

    def show(self):
        self.builder.get_object("main_window").show_all()

    def _create_object(self, _):
        self.dialog = self.builder.get_object("create_object_dialog")
        self.dialog.run()
        self.dialog.hide()

    def _dialog_ok(self, _):
        # TODO:
        # Read name from text entry and check if it already exists (if so, show error message on console)
        # Read points from active page (and get object type)
        # If line or wireframe, check for existence (same point / colinear?)
        # If wireframe, check pattern
        # Create object and add it to the world
        # Add object to TreeStore and make it visible

        if self.dialog:
            self.dialog.response(Gtk.ResponseType.OK)

    def _dialog_close(self, _):
        if self.dialog:
            self.dialog.response(Gtk.ResponseType.CLOSE)
