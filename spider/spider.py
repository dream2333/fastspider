from abc import ABCMeta, abstractmethod


# 爬虫类继承入口类
class Spider(metaclass=ABCMeta):
    def __init__(self) -> None:
        print("爬虫启动")

    @abstractmethod
    def start_requests(self):
        yield str


class TestSpider(Spider):
    def start_requests(self):
        for i in range(5):
            Request = {"url": "https://www.baidu.com/content-search.xml", "callback": "parse"}
            yield Request

    def parse(self, response):
        print(response)

if __name__ == "__main__":
    print(Spider())
