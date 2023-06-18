from fastspider.spider.spider import Spider
from example.testitem import Item
from fastspider.models import Request, Response


class ExampleSpider(Spider):
    def start_requests(self):
        print("第一层")
        for i in range(2):
            yield Request("https://www.baidu.com/content-search.xml")

    def parse(self, response: Response):
        print("第二层")
        yield Request("https://www.baidu.com/content-search.xml", callback="parse2")

    def parse2(self, response: Response):
        print(response.encoding)
        print("第三层")
        yield Item(url=response.url)
