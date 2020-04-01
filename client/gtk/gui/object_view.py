class ObjectView:
    def __init__(self, store, treeview):
        self._treeview = treeview
        treeview.set_model(store)

    @property
    def selected_object(self):
        """ Currently selected object in TreeView. """
        tree_model, tree_iter = self._treeview.get_selection().get_selected()
        if tree_iter is not None:
            return tree_model.get_value(tree_iter, 1) # TEMP: use ObjectStore enum instead
        else:
            return None
