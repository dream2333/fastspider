from asyncio import Queue as AsyncioQueue
from abc import ABCMeta, abstractmethod
from fastspider.utils import lazy_porperty
from aiokafka import AIOKafkaProducer

class Queue(metaclass=ABCMeta):
    @abstractmethod
    def put(self, obj):
        pass

    @abstractmethod
    def get(self):
        pass

class KafkaQueue(Queue):
    __slots__ = ("config",)
    def __init__(self,config) -> None:
        self.config = config

    @lazy_porperty
    def producer(self):
        self.producer = AIOKafkaProducer(bootstrap_servers="localhost:29092")

    def put(self, obj):
        
        pass

    def get(self):
        pass