from abc import ABCMeta, abstractmethod


class BasePipeline(metaclass=ABCMeta):
    @abstractmethod
    def process_item(self, item):
        ...
