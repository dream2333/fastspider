import asyncio
from concurrent.futures import ProcessPoolExecutor
from redis.asyncio import Redis as AsyncRedis
import time
from redis import Redis

redis = AsyncRedis(host="127.0.0.1", db=0)
# redis = Redis(host="127.0.0.1", db=0)
text = b"1234567890" * 1000

async def send():
    for i in range(1000):
        await redis.lpush("test", str(i))



async def main():
    await asyncio.gather(*[send() for i in range(10)])



def run():
    asyncio.run(main())


if __name__ == "__main__":
    # with ProcessPoolExecutor() as executor:
    #     start = time.monotonic()
    #     for i in range(1):
    #         executor.submit(run)
    #     executor.shutdown()
    # print(time.monotonic() - start)
    start = time.monotonic()
    asyncio.run(main())
    print(time.monotonic() - start)