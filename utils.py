class lazy_porperty:
    """
    一个装饰器类，允许函数进行惰性求值。
    只有在第一次访问属性时才会计算函数。
    """

    __slots__ = "func"

    def __init__(self, func) -> None:
        self.func = func

    def __get__(self, instance, cls):
        val = self.func(instance)
        setattr(instance, self.func.__name__, val)
        return val
