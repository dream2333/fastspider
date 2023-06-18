import asyncio
import os
from sre_compile import isstring
import sys

from fastspider.core.queue import AsyncioQueue
from fastspider.core.scheduler import Scheduler
from fastspider.pipeline import Pipeline
from fastspider.spider.loader import Loader
from fastspider.spider.spider import Spider


async def main(
    spider_name: str | Spider,
    pipelines: list[str | Pipeline] = None,
    spider_kwargs: dict = None,
):
    # 加载爬虫类

    spider_object = Loader.load_class(spider_name)
    pipeline_objects = []
    for pipeline in pipelines:
        if isstring(pipeline):
            _pipeline = Loader.load_class(pipeline)
            pipeline_objects.append(_pipeline())
        elif issubclass(pipeline, Pipeline):
            pipeline_objects.append(pipeline())
        else:
            raise TypeError(f"{pipeline} 不是Pipeline")
    async with Scheduler(
        spider_object(), AsyncioQueue(), AsyncioQueue(), pipeline_objects
    ) as scheduler:
        await scheduler.start_crawler()


def start():
    if os.name != "nt":
        import uvloop

        if sys.version_info >= (3, 11):
            with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
                runner.run(main())
        else:
            uvloop.install()
            asyncio.run(main())
    else:
        asyncio.run(main())


if __name__ == "__main__":
    start()
