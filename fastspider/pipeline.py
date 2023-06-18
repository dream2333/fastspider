from abc import abstractmethod, ABCMeta


class Pipeline(metaclass=ABCMeta):
    @abstractmethod
    def process_item(self, item):
        ...
