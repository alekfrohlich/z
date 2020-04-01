""" The ObjectFactory hierarchy enables the instantiation of the class Object
    without it beeing forced to do implementation-specific bookkeeping: i.e.,
    an Object should not need to know that it's creation has been logged or
    that the newly created object's name needs to appear in a widget. """

from abc import ABCMeta, abstractmethod


class ObjectStore(object):
    __metaclass__ = ABCMeta

    def __init__(self, window):
        self._wm = ObjectStore.WindowManager(window)

    class WindowManager:
        def __init__(self, window=None):
            self._window = window

        @property
        def current_window_name(self):
            return self._window.name

        @property
        def has_active_window(self):
            return self._window is not None

        def remove_window(self):
            self._window = None

        def set_window(self, window):
            self._window = window

        def to_window_coordinates(self, points):
            return self._window.window_transform(points)

    @abstractmethod
    def make_object(self, name, points): raise NotImplementedError

    @abstractmethod
    def remove_object(self, name): raise NotImplementedError
