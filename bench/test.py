import time
from aiokafka import AIOKafkaProducer
import asyncio

text = b"1234567891"*1000
with open("test.txt", "wb") as f:
    f.write(text)

async def send(times, producer: AIOKafkaProducer):
    for i in range(times):
        await producer.send("my_topic", text)
        # await producer.flush()


async def send_wait(times, producer: AIOKafkaProducer):
    for i in range(times):
        await producer.send_and_wait("my_topic", text)



async def main():
    producer = AIOKafkaProducer(bootstrap_servers="localhost:29092",)
    await producer.start()
    start = time.monotonic()
    await send(100000, producer)
    end = time.monotonic()
    print(end - start)
    await producer.stop()


asyncio.run(main())
