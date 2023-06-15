from asyncio import Queue
from abc import ABCMeta, abstractmethod

class BaseQueue(metaclass=ABCMeta):
    @abstractmethod
    def put(self, item):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def task_done(self):
        pass

    @abstractmethod
    def join(self):
        pass

    @abstractmethod
    def qsize(self):
        pass

    @abstractmethod
    def empty(self):
        pass

    @abstractmethod
    def full(self):
        pass