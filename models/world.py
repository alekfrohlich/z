""" Conceptual representation of the world as a list of objects. """


class World:

    _display_file = []

    @staticmethod
    def add_object(obj):
        World._display_file.append(obj)

    @staticmethod
    def objects():
        return World._display_file

    @staticmethod
    def size():
        return len(World._display_file)
