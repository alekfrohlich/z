""" Conceptual representation of the world as a list of objects. """

from models.object import Object


class World:
    _display_file = {}

    @staticmethod
    def add_object(obj):
        World._display_file[obj.name] = obj

    @staticmethod
    def objects():
        """ Display file. """
        return World._display_file

    @staticmethod
    def size():
        """ Size. """
        return len(World._display_file)
