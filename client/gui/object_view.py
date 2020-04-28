"""This module provides a thin wrapper for Gtk.TreeView.

Classes
-------
    ObjectView

"""
from ..object_store import Column


class ObjectView:
    """ObjectView class.

    Notes
    -----
        ObjectView is dependency injected by Gtk.Builder during
        GtkClient construction.

    """

    def __init__(self, store: 'ObjectStore', treeview: 'Gtk.TreeView'):
        """ObjectView constructor."""
        self._treeview = treeview
        treeview.set_model(store)

    def __len__(self):
        """Length of object store."""
        return len(self._treeview.get_model())

    @property
    def selected_object(self) -> 'str':
        """Currently selected object's name, if any."""
        tree_model, tree_iter = self._treeview.get_selection().get_selected()
        if tree_iter is not None:
            return tree_model.get_value(tree_iter, Column.NAME.value)
        else:
            return None
