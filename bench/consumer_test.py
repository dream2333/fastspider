from aiokafka import AIOKafkaConsumer
import asyncio



async def consume():
    consumer = AIOKafkaConsumer(
        "my_topic",
        bootstrap_servers="localhost:29092",
        client_id = "dream_test",
        group_id="my-group",
    )
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        consumer
        await consumer.seek_to_beginning()
        async for msg in consumer:
            ...
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()


asyncio.run(consume())
