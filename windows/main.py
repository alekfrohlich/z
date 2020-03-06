from gi.repository import Gtk

class MainWindow:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("layouts/main.glade")
        self.builder.get_object("viewport").set_size_request(500,500)

    def show(self):
        self.builder.get_object("main_window").show_all()
