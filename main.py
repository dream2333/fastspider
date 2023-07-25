import sys
from fastspider.core.engine import main
import asyncio


def suppress_keyboard_interrupt_message():
    old_except_hook = sys.excepthook

    def new_hook(exec_type, value, traceback):
        if exec_type != KeyboardInterrupt:
            old_except_hook(exec_type, value, traceback)
        else:
            print("\键盘中断 ...")

    sys.excepthook = new_hook


suppress_keyboard_interrupt_message()
spider_name = "example.spider.ExampleSpider"
pipelines_name = ["example.pipeline.ExamplePipeline1", "example.pipeline.ExamplePipeline2"]
asyncio.run(main(spider_name, pipelines_name))
