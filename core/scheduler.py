import asyncio
from typing import Callable, Generator, AsyncGenerator, Coroutine
from core.downloader import Downloader
from loguru import logger
from models.request import Request


class Scheduler:
    def __init__(self, spider_object) -> None:
        self.spider_object = spider_object
        self.request_queue = asyncio.Queue()
        self.downloader = Downloader()

    async def open_spider(self):
        spider_producer = self.add_requests_to_queue(None, "start_requests")
        spider_consumer = self.consumer()
        await asyncio.gather(spider_producer, spider_consumer)

    async def consumer(self):
        while True:
            request = await self.request_queue.get()
            # 消费Request，打包成task
            asyncio.create_task(self.next_request(request))

    async def add_requests_to_queue(self, response, cb_name):
        # 获取callback
        callback = getattr(self.spider_object, cb_name)
        # 判断是否为start_requests
        if response is None:
            rets = callback()
        else:
            rets = callback(response)
        if isinstance(rets, Generator):
            for ret in rets:
                if ret is not None:
                    await self.request_queue.put(ret)
        elif isinstance(rets, AsyncGenerator):
            async for ret in rets:
                if ret is not None:
                    await self.request_queue.put(ret)
        elif isinstance(rets, Coroutine):
            if await rets is not None:
                await self.request_queue.put(ret)
        elif isinstance(callback, Callable):
            if rets is not None:
                await self.request_queue.put(ret)

    async def next_request(self, request: Request):
        response = await self.downloader.request_with_session(request)
        logger.debug(response)
        if request.callback is None:
            await self.add_requests_to_queue(response, "parse")
        else:
            await self.add_requests_to_queue(response, request.callback)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.downloader.close()
