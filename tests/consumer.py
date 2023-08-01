from unittest import mock

import pytest

from kafka_adapter import KafkaConsumer, ConsumerSettings


@pytest.fixture(scope="function")
def consumer_settings() -> ConsumerSettings:
    return ConsumerSettings(
        bootstrap_servers="kafka_server",
        group_id="test_group_id"
    )


@pytest.fixture
def topics():
    return "test_topic"


@pytest.mark.asyncio
@mock.patch(
    "kafka_adapter.consumer.consumer.AIOKafkaConsumer",
    return_value=mock.AsyncMock(KafkaConsumer)
)
async def test_consumer(
    AIOKafkaConsumerMock,
    consumer_settings: ConsumerSettings,
    topics: str,
):
    await KafkaConsumer(consumer_settings=consumer_settings)._get_aiokafka_consumer(topics)
    AIOKafkaConsumerMock.assert_called_once()

    args, kwargs = AIOKafkaConsumerMock.call_args
    assert args[0] == topics
    assert kwargs.get("bootstrap_servers") == consumer_settings.bootstrap_servers
    assert kwargs.get("group_id") == consumer_settings.group_id
    assert kwargs.get("auto_commit_interval_ms") == consumer_settings.auto_commit_interval_ms
    assert kwargs.get("auto_offset_reset") == consumer_settings.auto_offset_reset
    assert kwargs.get("check_crcs") == consumer_settings.check_crcs
    assert kwargs.get("consumer_timeout_ms") == consumer_settings.consumer_timeout_ms
    assert kwargs.get("heartbeat_interval_ms") == consumer_settings.heartbeat_interval_ms
    assert kwargs.get("isolation_level") == consumer_settings.isolation_level
    assert kwargs.get("max_partition_fetch_bytes") == consumer_settings.max_partition_fetch_bytes
    assert kwargs.get("max_poll_interval_ms") == consumer_settings.max_poll_interval_ms
    assert kwargs.get("metadata_max_age_ms") == consumer_settings.metadata_max_age_ms
    assert kwargs.get("request_timeout_ms") == consumer_settings.request_timeout_ms
    assert kwargs.get("session_timeout_ms") == consumer_settings.session_timeout_ms
    assert kwargs.get("enable_auto_commit")
