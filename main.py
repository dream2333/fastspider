import asyncio
from math import log
from operator import call
from time import sleep
import uvloop
from core.downloader import Downloader
from timeit import default_timer as timer
import sys
from loguru import logger
from spider.loader import load_spider
from spider.spider import Spider
from contextvars import Context, ContextVar

# 加载爬虫类

SPIDER_NAME = "spider.spider.TestSpider"
spider_object = load_spider(SPIDER_NAME)


async def callback_producer(queue: asyncio.Queue, spider_object: Spider, response, cb_name="parse"):
    # 获取callback
    callback = getattr(spider_object, cb_name)
    # 生产url
    results = callback(response)
    if results is not None:
        for request in results:
            await queue.put(request)
            logger.debug(request)


async def start_producer(queue: asyncio.Queue, spider_object: Spider):
    # 获取callback
    callback = getattr(spider_object, "start_requests")
    # 生产url
    for request in callback():
        await queue.put(request)
        logger.debug(request)


async def consumer(queue, downloader: Downloader):
    while True:
        request = await queue.get()
        # 消费url，打包成task
        asyncio.create_task(get_response(queue, request, downloader))


async def get_response(queue, request, downloader: Downloader):
    response = await downloader.request_with_session(request["url"])
    logger.debug(response)
    await callback_producer(queue, spider_object, response, request["callback"])


async def main():
    async with Downloader() as downloader:
        # 内存队列
        queue = asyncio.Queue()
        spider_producer = start_producer(queue, spider_object)
        spider_consumer = consumer(queue, downloader)
        await asyncio.gather(spider_producer, spider_consumer)


if __name__ == "__main__":
    if sys.version_info >= (3, 11):
        with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
            runner.run(main())
    else:
        uvloop.install()
        asyncio.run(main())
