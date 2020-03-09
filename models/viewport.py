"""
    The Viewport is the region where the world (or a fraction of it) will be
    displayed. One Interactive Graphic System (IGS) can be connected to multiple
    viewports (e.g, the X window system).
"""

from abc import ABCMeta, abstractmethod

class ViewPort_Common:
    """ Common features present in all viewport implementations. """
    @abstractmethod
    def viewport_transform(self, points): raise NotImplementedError
