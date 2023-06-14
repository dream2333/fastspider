from msgspec import Struct
from abc import ABCMeta


class BaseItem(metaclass=ABCMeta):
    def __init__(self, name, price):
        ...

    def fingerprint(self):
        return "TODO"
