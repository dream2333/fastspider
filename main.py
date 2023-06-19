import sys
from fastspider.core.engine import main
import asyncio


def suppress_keyboard_interrupt_message():
    old_excepthook = sys.excepthook

    def new_hook(exctype, value, traceback):
        if exctype != KeyboardInterrupt:
            old_excepthook(exctype, value, traceback)
        else:
            print("\键盘中断 ...")

    sys.excepthook = new_hook
suppress_keyboard_interrupt_message()
spider_name = "example.spider.ExampleSpider"
pipelines_name = ["example.pipeline.ExamplePipeline1", "example.pipeline.ExamplePipeline2"]
asyncio.run(main(spider_name, pipelines_name))
