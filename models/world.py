""""""


class World:

    display_file = []

    @staticmethod
    def add_object(obj):
        World.display_file.append(obj)

    @staticmethod
    def objects():
        return World.display_file

    @staticmethod
    def size():
        return len(World.display_file)