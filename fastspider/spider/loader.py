from importlib import import_module
from typing import Any


class Loader:
    @staticmethod
    def load_class(path: str) -> Any:
        """
        从指定路径中加载类对象。

        Args:
            path (str): 类路径，例如 'module.submodule.ClassName'

        Returns:
            Any: 加载的类对象

        Raises:
            ValueError: 如果路径不完整
            NameError: 如果模块中没有定义指定的类
        """

        try:
            dot = path.rindex(".")
        except ValueError:
            raise ValueError(f"加载 '{path}' 失败: 路径不完整")
        module, name = path[:dot], path[dot + 1 :]
        mod = import_module(module)
        try:
            class_obj = getattr(mod, name)
        except AttributeError:
            raise NameError(f"模块 '{module}' 没有定义任何名为 '{ name}' 的类")
        return class_obj
