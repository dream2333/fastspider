import cProfile
import io
from multiprocessing import Process
import pstats
import time
from aiokafka import AIOKafkaProducer
import asyncio




async def send_many():
    text = b"1234567891" * 1000
    producer = AIOKafkaProducer(
        bootstrap_servers="localhost:29092",
        max_batch_size=65535,
        linger_ms=5
    )

    pr = cProfile.Profile()
    pr.enable()

    await producer.start()

    total_sent = 0
    started = time.time()

    for i in range(10000):
        await producer.send("test_topic_aiokafka", value=text)
    await producer.stop()

    pr.disable()
    s = io.StringIO()
    sortby = "cumtime"
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())


def send_many_main():
    asyncio.run(send_many())


send_many_main()
