import datetime
from multiprocessing.reduction import send_handle
import time
from aiokafka import AIOKafkaProducer
import asyncio

text = b"1234567891"


async def send(times, producer: AIOKafkaProducer):
    for i in range(times):
        f = await producer.send("my_topic", text)


async def send_wait(times, producer: AIOKafkaProducer):
    for i in range(times):
        await producer.send_and_wait("my_topic", text)


async def send_batch(times, producer: AIOKafkaProducer):
    batch = producer.create_batch()
    for i in range(times):
        batch.append(key=None, timestamp=None, value=text)
    print(await producer.send_batch(batch, "my_topic", partition=None))
    await asyncio.sleep(100)


async def main():
    producer = AIOKafkaProducer(bootstrap_servers="localhost:29092")
    await producer.start()
    start = time.monotonic()
    await send(100000, producer)
    end = time.monotonic()
    print(end - start)
    await producer.stop()


asyncio.run(main())
