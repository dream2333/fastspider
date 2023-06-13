from spider.spider import Spider

from models import Request, Response

class TestSpider(Spider):
    async def start_requests(self):
        print("第一层")
        for i in range(2):
            yield Request(
                "https://www.baidu.com/content-search.xml",
            )

    async def parse(self, response:Response):
        print("第二层")
        yield Request("https://www.baidu.com/content-search.xml", callback="parse2")

    async def parse2(self, response:Response):
        text = await response.text()
        print(text)
        print("第三层")

