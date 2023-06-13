from abc import ABCMeta, abstractmethod


# 爬虫类继承入口类
class Spider(metaclass=ABCMeta):
    def __init__(self) -> None:
        print("爬虫启动")

    @abstractmethod
    def start_requests(self):
        yield None


if __name__ == "__main__":
    print(Spider())
