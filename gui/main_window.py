""" Main application window (Gtk3 - Glade). """

from gi.repository.Gtk import main_quit
from gi.repository.Gtk import Builder
from gi.repository.Gtk import ResponseType

from core import DirectionType
from core.log import Logger, LogLevel
from gui.dialogs import CreateObjectDialog
from gui.viewport import ViewPort
from models.world import World
from models.window import Window


class MainWindow:
    """
        Main GUI window, has access to glade builder and thus is responsible
        for passing it around to other Glade-related graphical components.
    """

    def needs_redraw(f):
        """ Decorates methods that modify the display file and thus demand it
            to be redrawn to take effect. """
        def wrapper(self, *args, **kwargs):
            f(self, *args, **kwargs)
            self._builder.get_object("viewport").queue_draw()
        return wrapper

    def __init__(self):
        self._builder = Builder()
        self._builder.add_from_file("glade/z_gui_layout.glade")
        self._builder.get_object("viewport").set_size_request(
            *ViewPort.RESOLUTION)

        self._store = self._builder.get_object("object_list_store")
        self._builder.get_object("object_list").set_model(self._store)

        self._create_object_dialog = CreateObjectDialog(self._builder,
                                                        self._store)
        self._viewport = ViewPort(self._builder)
        handlers = {
            "on_destroy": main_quit,
            # Controls
            "on_up_button": lambda _ : self._on_move_window(DirectionType.UP),
            "on_left_button":  lambda _ : self._on_move_window(DirectionType.LEFT),
            "on_right_button": lambda _ : self._on_move_window(DirectionType.RIGHT),
            "on_down_button":  lambda _ : self._on_move_window(DirectionType.DOWN),
            "on_zoom_in":  lambda _ : self._on_zoom_window(inwards=True),
            "on_zoom_out": lambda _ : self._on_zoom_window(inwards=False),
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

    # Attributes

    @property
    def step(self):
        tmp = self._builder.get_object("step_entry").get_text()
        return int(tmp)

    # GUI buttons

    @needs_redraw
    def _on_create_object(self, _):
        """ Show 'Create object' dialog and wait for it's response. Note that
            if successful the display is hidden again (not destroyed). """
        response = self._create_object_dialog.run()
        Logger.log(LogLevel.INFO, "Dialog returned with response code "
                   + str(ResponseType(response)))

        if response == ResponseType.OK:
            obj = World.make_object(self._create_object_dialog.name,
                                    self._create_object_dialog.points)
            self._store.append([obj.name, str(obj.type)])
        self._create_object_dialog.hide()

    @needs_redraw
    def _on_move_window(self, direction):
        """ Move (see core.DirectionType) the window by offset specified in the
            control menu. """
        x_offset, y_offset = direction.value
        Window.move(x_offset * self.step, y_offset * self.step)

    @needs_redraw
    def _on_zoom_window(self, inwards):
        """ Zoom (in or out) the window by offset specificed in the control
            menu (step taken as percentage). """
        scale = (1 + self.step/100) ** (-1 if inwards else 1)

        new_x_max = Window.x_max * scale
        new_x_min = Window.x_min * scale
        new_y_max = Window.y_max * scale
        new_y_min = Window.x_min * scale

        if new_x_max - new_x_min < 10 or new_y_max - new_y_min < 10: # too small
            Logger.log(LogLevel.WARN, "Zoom limited exceeded, further zooming will be surpressed!")
        else:
            Window.x_max = new_x_max
            Window.x_min = new_x_min
            Window.y_max = new_y_max
            Window.y_min = new_y_min
