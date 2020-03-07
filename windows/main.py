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
            "on_create_wireframe": self._create_wireframe,
        }
        self.builder.connect_signals(handlers)

    def fixme(self, _):
        print("Feature not yet implemented!")

    def show(self):
        self.builder.get_object("main_window").show_all()

    def _create_wireframe(self, _):
        print("Wireframe do favarin!")