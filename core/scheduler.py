import asyncio
from typing import Callable, Generator, AsyncGenerator, Coroutine
from core.downloader import Downloader
from loguru import logger
from models import Request, Response, BaseItem
from core.queue import BaseQueue
import settings


class Scheduler:
    def __init__(self, spider_object,queue:BaseQueue) -> None:
        self.spider_object = spider_object
        self.request_queue = queue
        self.item_queue = queue
        self.downloader = Downloader()
        self.pipelines = self.create_pipelines(settings.PIPELINES)

    def create_pipelines(self, pipelines):
        return [pipeline() for pipeline in pipelines]

    async def start_crawler(self):
        spider_producer = self.add_requests_items_to_queue(None, "start_requests")
        request_consumer = self.start_process_requests()
        item_consumer = self.start_process_item()
        await asyncio.gather(spider_producer, request_consumer, item_consumer)

    async def start_process_requests(self):
        while True:
            request = await self.request_queue.get()
            asyncio.create_task(self.download_request(request))

    async def start_process_item(self):
        while True:
            item = await self.item_queue.get()
            asyncio.create_task(self.send_item_to_pipe(item))

    async def add_requests_items_to_queue(self, response: Response, cb_name: str):
        # 获取callback
        callback = getattr(self.spider_object, cb_name)
        # 判断是否为start_requests
        if response is None:
            rets = callback()
        else:
            rets = callback(response)
        if isinstance(rets, Generator):
            for ret in rets:
                if ret is None:
                    return
                elif isinstance(ret, Request):
                    await self.request_queue.put(ret)
                elif isinstance(ret, BaseItem):
                    await self.item_queue.put(ret)
        elif isinstance(rets, AsyncGenerator):
            async for ret in rets:
                if ret is None:
                    return
                elif isinstance(ret, Request):
                    await self.request_queue.put(ret)
                elif isinstance(ret, BaseItem):
                    await self.item_queue.put(ret)
        elif isinstance(rets, Coroutine):
            if await rets is None:
                return
            elif isinstance(rets, Request):
                await self.request_queue.put(ret)
            elif isinstance(rets, BaseItem):
                await self.item_queue.put(ret)
        elif isinstance(callback, Callable):
            if rets is None:
                return
            elif isinstance(rets, Request):
                await self.request_queue.put(ret)
            elif isinstance(rets, BaseItem):
                await self.item_queue.put(ret)

    async def download_request(self, request: Request):
        logger.debug(request)
        response = await self.downloader.request_with_session(request)
        if request.callback is None:
            await self.add_requests_items_to_queue(response, "parse")
        else:
            await self.add_requests_items_to_queue(response, request.callback)

    async def send_item_to_pipe(self, item: BaseItem):
        for pipeline in self.pipelines:
            if isinstance(pipeline.process_item, Coroutine):
                item = await pipeline.process_item(item)
            elif isinstance(pipeline.process_item, Callable):
                item = pipeline.process_item(item)
            # 如果pipeline返回None则不再继续处理
            if item is None:
                break

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.downloader.close()
