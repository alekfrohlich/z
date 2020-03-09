""" Glade parser """

from gi.repository.Gtk import main_quit
from gi.repository.Gtk import Builder
from gi.repository.Gtk import ResponseType
from gi.repository.Gtk import CellRendererText, ListStore, TreeViewColumn

from core.log import Logger, LogLevel
from core.object_factory import ObjectFactory
from models.world import World
from gui.dialogs import CreateObjectDialog


class MainWindow:
    # TODO:
    # Design ListStore with Glade

    def __init__(self):
        self._builder = Builder()
        self._builder.add_from_file("glade/z_gui_layout.glade")
        self._builder.get_object("viewport").set_size_request(500,500)

        self._store = ListStore(str, str)
        self._builder.get_object("object_list").set_model(self._store)
        self._builder.get_object("object_list").append_column(
            TreeViewColumn("Name", CellRendererText(), text=0))
        self._builder.get_object("object_list").append_column(
            TreeViewColumn("Type", CellRendererText(), text=1))

        self._create_object_dialog = CreateObjectDialog(self._builder, self._store)
        handlers = {
            "on_destroy" : main_quit,
            "on_draw": self._on_draw,
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
        self._builder.connect_signals(handlers)


    def fixme(self, _):
        print("Feature not yet implemented!")

    def show(self):
        """ Display application window. """
        self._builder.get_object("main_window").show_all()

    def _on_create_object(self, _):
        """ Display 'Create object' dialog and wait for it's response. """
        response = self._create_object_dialog.run()
        Logger.log(LogLevel.INFO, "Dialog returned with response code " + str(ResponseType(response)))

        if response == ResponseType.OK:
            obj = ObjectFactory.make_object(self._create_object_dialog.name,
                self._create_object_dialog.points)
            self._store.append([obj.name, str(obj.type)])
            self._builder.get_object("viewport").queue_draw()

        self._create_object_dialog.hide()

    def _on_draw(self, _, ctx):
        ctx.set_line_width(2)
        ctx.set_source_rgb(0, 0, 0)
        for obj in World.objects():
            points = obj.points
            ctx.move_to(*points[0])
            for point in points[1:]:
                ctx.line_to(*point)
        ctx.stroke()