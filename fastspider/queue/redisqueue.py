from fastspider.utils import lazy_proxy, AioInitMixin
from fastspider.queue.queue import Queue

# from aiokafka import AIOKafkaProducer
from redis import asyncio as aioredis
from redis import exceptions as redis_exceptions

import platform
import os


class RedisQueue(Queue, AioInitMixin):
    async def __init__(
        self, spidername: str, buffer: int = 10, *args, **kwargs
    ) -> None:
        self.client = aioredis.Redis(*args, **kwargs)
        self.spider_name = spidername
        self.group_name = "spider"
        self.buffer = buffer
        client_info = await self.client.client_info()
        self.workername = f"[{os.getpid()}]{platform.node()}/{client_info['addr']}"
        try:
            await self.client.xgroup_create(spidername, self.group_name, mkstream=True)
        except redis_exceptions.ResponseError as e:
            print("消费者组已存在")

    async def get(self):
        while True:
            messages = await self.client.xreadgroup(
                self.group_name,
                self.workername,
                {self.spider_name: ">"},
                count=self.buffer,
                block=1000,
            )
            if messages:
                return messages

    async def put(self, obj):
        await self.client.xadd(self.spider_name, obj, nomkstream=True)


if __name__ == "__main__":
    import asyncio

    async def main():
        queue = await RedisQueue("test_spider", host="127.0.0.1", port=6379, db=0)
        # await queue.put({"url": "http://www.baidu.com"})
        msg = await queue.get()
        print(msg)

    asyncio.run(main())
