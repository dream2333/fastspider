class lazy_proxy:
    """
    描述符装饰器，允许函数进行惰性求值。
    只有在第一次访问属性时才会计算。
    """

    __slots__ = "func"

    def __init__(self, func) -> None:
        self.func = func

    def __get__(self, instance, cls):
        val = self.func(instance)
        setattr(instance, self.func.__name__, val)
        return val


class AioInitMixin:
    """
    mixin类
    允许类使用异步的__init__方法
    """

    async def __new__(cls, *a, **kw):
        instance = super().__new__(cls)
        await instance.__init__(*a, **kw)
        return instance

    async def __init__(self):
        pass
