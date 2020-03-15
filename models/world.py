""" Conceptual representation of the world as a list of objects. """


class World:
    def __init__(self):
        self._display_file = {}

    # make world accessible by object

    def add_object(self, obj):
        """ Adds world to display file (dict). """
        self._display_file[obj.name] = obj

    def objects(self):
        """ Objects. """
        return self._display_file

    def size(self):
        """ Number of objects in the world. """
        return len(self._display_file)
