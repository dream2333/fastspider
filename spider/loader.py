from importlib import import_module
from spider.spider import Spider


class SpiderLoader:
    @staticmethod
    def load_spider(spider_name: str) -> Spider:
        """
        根据给定的名称加载一个 Spider 对象。

        Args:
        spider_name (str): 要加载的 Spider 对象的名称。

        Returns:
        Spider: 加载的 Spider 对象。

        Raises:
        ValueError: 如果 Spider 名称不是完整路径。
        NameError: 如果模块没有定义指定的 Spider 对象。
        """
        spider_class = SpiderLoader.load_object(spider_name)
        spider_object = spider_class()
        return spider_object

    @staticmethod
    def load_object(path: str):
        """
        从指定路径中加载对象并返回该对象。

        Args:
        path (str): 对象的完整路径，例如'module.submodule.object'。

        Returns:
        object: 加载的对象。

        Raises:
        ValueError: 如果路径不完整，则引发此异常。
        NameError: 如果模块中没有定义指定的对象，则引发此异常。
        """
        try:
            dot = path.rindex(".")
        except ValueError:
            raise ValueError(f"加载 '{path}' 失败: 路径不完整")
        module, name = path[:dot], path[dot + 1 :]
        mod = import_module(module)
        try:
            obj = getattr(mod, name)
        except AttributeError:
            raise NameError(f"模块 '{module}' 没有定义任何名为 '{ name}' 的类")
        return obj
