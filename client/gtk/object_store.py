""" """

from util.log import Logger, LogLevel
from objects.object import Object
from client.object_store import ObjectStore
from client.gtk.gui.viewport import ViewPort


class GtkObjectStore(ObjectStore):
    # REPARTIR EM VIEW - STORE
    def __init__(self, display_file, store, treeview, viewport, window_manager):
        self._display_file = display_file
        self._treeview = treeview
        self._store = store
        self._viewport = viewport
        self._window_manager = window_manager

    @property
    def default_object_name(self):
        """ Default name for anonymous objects. """
        return "object{}".format(len(self._display_file))

    @property
    def selected_object(self):
        """ Currently selected object in TreeView. """
        tree_model, tree_iter = self._treeview.get_selection().get_selected()
        if tree_iter is not None:
            return tree_model.get_value(tree_iter, 0)
        else:
            return None

    @ViewPort.needs_redraw
    def make_object(self, name, points, color=(0.0, 0.0, 0.0)):
        """ Creates new object and adds it to the world. The returned object is
            not owned by the caller, so weird things will happen if it is
            modified. """
        if name == "":
            name = self.default_object_name
        obj = Object(name, points, color)
        self._store.append([obj.name, str(obj.type)])
        self._display_file[name] = obj
        Logger.log(LogLevel.INFO, obj)
        return obj

    @ViewPort.needs_redraw
    def remove_object(self, name):
        """ Removes object from the world. """
        for row in self._store:
            if row[0] == name:
                self._store.remove(row.iter)
                break
        del self._display_file[name]
        if self._window_manager.current_window_name == name:
            self._window_manager.remove_window()
        Logger.log(LogLevel.INFO, name + " has been removed!")

    @ViewPort.needs_redraw
    def translate(self, dx, dy):
        """ Translate the selected object by the offset specified in the
            control menu. If there is no such object, translates the window
            instead. """
        if self.selected_object is not None:
            self._display_file[self.selected_object].translate(dx, dy)

    @ViewPort.needs_redraw
    def scale(self, factor):
        """ Scales the selected object by the factor specified in the control
            menu. If there is no selected object, scales the window
            instead. """
        if self.selected_object is not None:
            self._display_file[self.selected_object].scale(factor, factor)

    @ViewPort.needs_redraw
    def rotate(self, rads, point):
        """ Rotates the selected object in respect to the given point
            by the amount specified in the control menu. If there
            is no selected object, translates the window instead. """
        if self.selected_object is not None:
            self._display_file[self.selected_object].rotate(rads, point)
