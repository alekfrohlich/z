from gi.repository import Gtk

# TODO:
# Implement handlers

class MainWindow:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("layouts/release01.glade")
        self.builder.get_object("viewport").set_size_request(500,500)
        handlers = {
            "on_destroy" : Gtk.main_quit,
            "on_draw": self.dummy,
            "on_button_up_clicked": self.dummy,
            "on_button_down_clicked":  self.dummy,
            "on_button_left_clicked":  self.dummy,
            "on_button_right_clicked": self.dummy,
            "on_zoom_in":  self.dummy,
            "on_zoom_out": self.dummy,
            # menu bar buttons
            "on_menu_bar_quit": Gtk.main_quit,
            "on_create_wireframe": self.dummy,
        }
        self.builder.connect_signals(handlers)

    def dummy(self):
        print("hello!")

    def show(self):
        self.builder.get_object("main_window").show_all()
