from spider.spider import Spider

from models import Request, Response

class TestSpider(Spider):
    def start_requests(self):
        print("第一层")
        for i in range(2):
            yield Request(
                "https://www.baidu.com/content-search.xml",
            )

    def parse(self, response:Response):
        print("第二层")
        yield Request("https://www.baidu.com/content-search.xml", callback="parse2")

    def parse2(self, response:Response):
        text = response.text
        print(text)
        print("第三层")

