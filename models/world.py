""""""


class World:

    DISPLAY_FILE = []

    @staticmethod
    def add_object(obj):
        World.DISPLAY_FILE.append(obj)

    @staticmethod
    def objects():
        return World.DISPLAY_FILE
