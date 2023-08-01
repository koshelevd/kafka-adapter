import asyncio

from kafka_adapter import KafkaProducer, ProducerEvent, ProducerSettings

init_producer = KafkaProducer(
    producer_settings=ProducerSettings(
        bootstrap_servers="127.0.0.1:9092",
        acks="all",
        transactional_id="test-transactional-id",
    )
)

producer_event = ProducerEvent(topic="TEST-TOPIC", value={"TEST": "test"})
asyncio.run(init_producer.start(producer_event=producer_event))
