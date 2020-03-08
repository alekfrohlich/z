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
        self.dialog = self.builder.get_object("create_object_dialog")

    def fixme(self, _):
        print("Feature not yet implemented!")

    def show(self):
        self.builder.get_object("main_window").show_all()

    def _create_object(self, _):
        """ Display 'Create object' dialog and wait for it's response. """
        self.dialog.run() # Log response type
        self.dialog.hide()

    def _dialog_ok(self, _) -> bool:
        """ Check if form input is valid. If so, create new object with it. """
        # Read name from text entry and check if it already exists (if so, show error message on console)
        object_name = self.builder.get_object("name_dialog_field").get_text()
        if object_name == "asd":
            # Log to console
            print("Object name: " + object_name + " already taken!")
            return False

        # Read points from active page (and get object type)
        stack = self.builder.get_object("object_type_stack")
        page = stack.get_visible_child()
        page_name = page.get_name()

        if page_name == "point_page":
            x = int(self.builder.get_object("point_x").get_text())
            y = int(self.builder.get_object("point_y").get_text())
            z = int(self.builder.get_object("point_z").get_text())
            print("Point object at " + str((x,y,z)))

        elif page_name == "line_page":
            x1 = int(self.builder.get_object("line_x1").get_text())
            y1 = int(self.builder.get_object("line_y1").get_text())
            z1 = int(self.builder.get_object("line_z1").get_text())
            x2 = int(self.builder.get_object("line_x2").get_text())
            y2 = int(self.builder.get_object("line_y2").get_text())
            z2 = int(self.builder.get_object("line_z2").get_text())
            print("Line object from " + str((x1,y1,z1)) + " to " + str((x2,y2,z2)))
            # Verify if inside world and if not equal
            if (x1,y1,z1) == (x2, y2, z2):
                print("Two equal points cannot compose a line!")
                return False

        elif page_name == "wireframe_page":
            wireframe_expression = self.builder.get_object("wireframe_expression").get_text()
            print("Wireframe at " + wireframe_expression)
            # Verify expression and check if colinear

        else: # curves_page
            print("Curves not yet implemented!")
            return False

        # TODO:
        # Create object and add it to the world
        # Add object to TreeStore and make it visible

        self.dialog.response(Gtk.ResponseType.OK)

    def _dialog_close(self, _):
        """ Closes dialog without creating object. """
        self.dialog.response(Gtk.ResponseType.CLOSE)
