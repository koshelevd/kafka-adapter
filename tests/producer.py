import pytest
from unittest import mock
from uuid import UUID

from kafka_adapter import KafkaProducer, ProducerEvent, ProducerSettings


@pytest.fixture(scope="function")
def producer_setting() -> ProducerSettings:
    return ProducerSettings(
        acks="all",
        bootstrap_servers="kafka_server",
        transactional_id="test_transactional_id"
    )


@pytest.fixture(scope="function")
def producer_event() -> ProducerEvent:
    return ProducerEvent(
        topic="test_topic_name",
        value={"test": "value"}
    )


@pytest.mark.asyncio
@mock.patch(
    "kafka_adapter.producer.producer.AIOKafkaProducer",
    return_value=mock.AsyncMock(KafkaProducer)
)
async def test_producer(
        AIOKafkaProducerMock,
        producer_setting: ProducerSettings,
        producer_event: ProducerEvent
):
    producer = KafkaProducer(producer_settings=producer_setting)
    await producer.start(producer_event=producer_event)

    args, kwargs = AIOKafkaProducerMock.call_args
    assert AIOKafkaProducerMock.call_count == 1
    assert isinstance(producer.serializer(producer_event.value), bytes)
    assert kwargs.get("acks") == producer_setting.acks
    assert kwargs.get("bootstrap_servers") == producer_setting.bootstrap_servers
    assert kwargs.get("transactional_id") == producer_setting.transactional_id

    args, kwargs = AIOKafkaProducerMock.return_value.send_and_wait.call_args
    assert kwargs.get("topic") == producer_event.topic
    assert kwargs.get("value") == producer_event.value
    assert isinstance(kwargs.get("key"), UUID)
