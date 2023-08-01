import asyncio

from kafka_adapter import KafkaConsumer, ConsumerSettings


consumer_settings = ConsumerSettings(
    bootstrap_servers="127.0.0.1:9092",
    group_id="test-group-id"
)


async def message_handler(message):
    print(message)
    print('Raising exception in message handler...')
    raise Exception('Test exception')

consumer = KafkaConsumer(consumer_settings=consumer_settings)

# asyncio.run(consumer.register_simple_event(topics="TEST-TOPIC", message_handler=message_handler))
asyncio.run(consumer.register_durable_event(
    topics="TEST-TOPIC",
    message_handler=message_handler,
    retry_topic="Test-retry-topic",
    retry_count=3,
    retry_timeout=900,
))
