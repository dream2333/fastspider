import asyncio
import sys
import aiohttp
import uvloop
from loguru import logger
from concurrent.futures import ProcessPoolExecutor


def get_abuyun_proxy():
    key = "60CF0837"
    passwd = "C29A6926638C"
    proxyHost = "tunnel2.qg.net"
    proxyPort = "18423"
    proxy = "http://{}:{}@{}:{}".format(key, passwd, proxyHost, proxyPort)
    return proxy


URL = "http://www.baidu.com/content-search.xml"


async def fetch_async():
    try:
        async with aiohttp.request("GET", url=await queue.get(), proxy=proxy) as response:
            asyncio.create_task(response.text())

    except Exception as e:
        logger.error(e)
        ...

async def add_urls():
    while True:
        await asyncio.sleep(0.01)
        await queue.put(URL)

async def main():
    global  queue, sem, proxy,connector
    queue = asyncio.Queue(1000)
    sem = asyncio.Semaphore(500)
    connector = aiohttp.TCPConnector(limit=500, ssl=False)
    proxy = get_abuyun_proxy()
    await asyncio.gather(add_urls(),fetch_async())


def run():
    if sys.version_info >= (3, 11):
        with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
            runner.run(main())
    else:
        uvloop.install()
        asyncio.run(main())


if __name__ == "__main__":
    with ProcessPoolExecutor() as pool:
        for i in range(6):
            pool.submit(run)
        pool.shutdown()