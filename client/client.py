""""""

from abc import ABCMeta, abstractmethod


class Client(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def quit(self): raise NotImplementedError

    @abstractmethod
    def run(self): raise NotImplementedError
