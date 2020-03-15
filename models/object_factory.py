""" The ObjectFactory hierarchy enables the instantiation of the class Object
    without it beeing forced to do implementation-specific bookkeeping: i.e.,
    an Object should not need to know that it's creation has been logged or
    that the newly created object's name needs to appear in a widget. """

from abc import ABCMeta, abstractmethod


class ObjectFactory(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def make_object(self, name, points): raise NotImplementedError

    @abstractmethod
    def remove_object(self, name): raise NotImplementedError

    @abstractmethod
    def default_object_name(self, name, points): raise NotImplementedError
