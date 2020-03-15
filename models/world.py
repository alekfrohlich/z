""" Conceptual representation of the world as a list of objects. """


class World:
    def __init__(self):
        self._display_file = {}

    def __contains__(self, name):
        """ Test containership in the world. """
        return name in self._display_file

    def __delitem__(self, key):
        """ Removes object from the world. """
        self._display_file.pop(key)

    def __getitem__(self, key):
        """ Restrict assignment and make accesing a specific world object
            more convenient. """
        return self._display_file[key]

    def __setitem__(self, key, value):
        """ Adds world to display file (dict). """
        self._display_file[key] = value

    def objects(self):
        """ Objects. """
        return self._display_file

    def size(self):
        """ Number of objects in the world. """
        return len(self._display_file)
