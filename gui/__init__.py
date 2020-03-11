""""""

from core.log import Logger, LogLevel


class ObjectFactory:
    def __init__(self, store):
        self._store = store

    def make_object(self, name, points):
        obj = World.make_object(name, point)
        self._store.append([obj.name, str(obj.type)])
        Logger.log(LogLevel.INFO, obj)
