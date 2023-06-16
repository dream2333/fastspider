import asyncio
import sys
from core.queue import AsyncioQueue
import uvloop
from core.scheduler import Scheduler
from spider.loader import SpiderLoader


async def main():
    # 加载爬虫类
    SPIDER_NAME = "tests.testspider.TestSpider"
    spider_object = SpiderLoader.load_spider(SPIDER_NAME)
    async with Scheduler(spider_object, AsyncioQueue()) as scheduler:
        await scheduler.start_crawler()


def suppress_keyboard_interrupt_message():
    old_excepthook = sys.excepthook

    def new_hook(exctype, value, traceback):
        if exctype != KeyboardInterrupt:
            old_excepthook(exctype, value, traceback)
        else:
            print("\键盘中断 ...")

    sys.excepthook = new_hook


if __name__ == "__main__":
    suppress_keyboard_interrupt_message()
    if sys.version_info >= (3, 11):
        with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
            runner.run(main())
    else:
        uvloop.install()
        asyncio.run(main())
