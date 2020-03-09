""" Main application window (Gtk3 - Glade). """

from gi.repository.Gtk import main_quit
from gi.repository.Gtk import Builder
from gi.repository.Gtk import ResponseType
from gi.repository.Gtk import CellRendererText, ListStore, TreeViewColumn

from core.log import Logger, LogLevel
from core.object_factory import ObjectFactory
from gui.dialogs import CreateObjectDialog
from gui.viewport import ViewPort


class MainWindow:
    """
        Main GUI window, has access to glade builder and thus is responsible
        for passing it around to other Glade-related graphical components.
    """

    def __init__(self):
        self._builder = Builder()
        self._builder.add_from_file("glade/z_gui_layout.glade")
        self._builder.get_object("viewport").set_size_request(500,500)

        self._store = self._builder.get_object("object_list_store")
        self._builder.get_object("object_list").set_model(self._store)

        self._create_object_dialog = CreateObjectDialog(self._builder, self._store)
        self._viewport = ViewPort(self._builder)
        handlers = {
            "on_destroy" : main_quit,
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
            "on_create_object": self._on_create_object,
        }
        handlers.update(self._create_object_dialog.handlers)
        handlers.update(self._viewport.handlers)
        self._builder.connect_signals(handlers)


    def fixme(self, _):
        print("Feature not yet implemented!")

    def show(self):
        """ Display application window. """
        self._builder.get_object("main_window").show_all()

    # GUI buttons

    def _on_create_object(self, _):
        """ Display 'Create object' dialog and wait for it's response. """
        response = self._create_object_dialog.run()
        Logger.log(LogLevel.INFO, "Dialog returned with response code " + str(ResponseType(response)))

        if response == ResponseType.OK:
            obj = ObjectFactory.make_object(self._create_object_dialog.name,
                self._create_object_dialog.points)
            self._store.append([obj.name, str(obj.type)])
            self._viewport.update()

        self._create_object_dialog.hide()
