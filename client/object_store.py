""" The ObjectStore type hierarchy is reponsible for abstracting how objects
    are stored. """

from abc import ABCMeta, abstractmethod


class ObjectStore(object):
    __metaclass__ = ABCMeta
    """Base class that provides the standard interface for accessing objects."""

    class WindowManager:
        """ The WindowManager keeps track of which object, if any, currently
            represents the window. Also helps changing coordinates systems
            from World to Window. """
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

    def __init__(self, window):
        self._wm = ObjectStore.WindowManager(window)

    @abstractmethod
    def __getitem__(self, key): raise NotImplementedError

    @abstractmethod
    def make_object(self, name, points): raise NotImplementedError

    @abstractmethod
    def remove_object(self, name): raise NotImplementedError
