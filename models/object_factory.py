""""""

from abc import ABCMeta, abstractmethod


class ObjectFactory(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def make_object(self, name, points): raise NotImplementedError

    @abstractmethod
    def default_object_name(self, name, points): raise NotImplementedError
