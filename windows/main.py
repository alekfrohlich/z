""""""
from gi.repository.Gtk import Builder, ResponseType, main_quit

from core.log import Logger, LogLevel
from windows.dialogs import CreateObjectDialog


class MainWindow:
    def __init__(self):
        self.builder = Builder()
        self.builder.add_from_file("glade/z_gui_layout.glade")
        self.builder.get_object("viewport").set_size_request(500,500)
        self.create_object_dialog = CreateObjectDialog(self.builder)
        handlers = {
            "on_destroy" : main_quit,
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
            "on_menu_bar_quit": main_quit,
            "on_create_object": self._create_object,
        }
        handlers.update(self.create_object_dialog.handlers)
        self.builder.connect_signals(handlers)

    def fixme(self, _):
        print("Feature not yet implemented!")

    def show(self):
        """ Display application window. """
        self.builder.get_object("main_window").show_all()

    def _create_object(self, _):
        """ Display 'Create object' dialog and wait for it's response. """
        response = self.create_object_dialog.run()
        Logger.log(LogLevel.INFO, "Dialog returned with response code " + str(ResponseType(response)))
        self.create_object_dialog.hide()
