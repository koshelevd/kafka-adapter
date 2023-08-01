## _KAFKA-ADAPTER ДЛЯ ОБРАБОТКИ СОБЫТИЙ_ (kafka-adapter)

> [AIOKafka docs](https://aiokafka.readthedocs.io/en/stable/index.html)
> 
> [AIOKafka github](https://github.com/aio-libs/aiokafka/blob/master/docs/index.rst?ysclid=lhhpdli18055842377)

***************************************************
Настройки проекта.
***************************************************
```sh
from pydantic import BaseModel


class Settings(BaseModel):
    kafka_server: str = "localhost:9092"
    kafka_topic: str = "TEST-SAGA"
    transactional_id = "TEST-TRANS-ID"
    kafka_acks: str = "all"
    group_id: str = "Test_group"
```

***************************************************
Работа с продюсером через делегат.
***************************************************
```sh
import asyncio

from kafka_adapter import KafkaProducer, ProducerEvent, ProducerSettings


kafka_settings = Settings()

init_producer = KafkaProducer(
    producer_settings=ProducerSettings(
        acks=kafka_settings.kafka_acks,
        bootstrap_servers=kafka_settings.kafka_server,
        transactional_id=kafka_settings.transactional_id
    )
)

producer_event = ProducerEvent(topic=kafka_settings.kafka_topic, value={"Test": "test"})
asyncio.run(init_producer.start(producer_event=producer_event))
```
***************************************************
Работа с консьюмером через делегат.
***************************************************
```sh
import asyncio

from kafka_adapter import KafkaConsumer, ConsumerSettings


kafka_settings = Settings()

consumer_settings = ConsumerSettings(
    bootstrap_servers=kafka_settings.kafka_server,
    group_id=kafka_settings.group_id,
)

class KafkaMessageDTO(BaseModel):
    Test: str

async def message_handler(message):
    print(KafkaMessageDTO(**message))

consumer = KafkaConsumer(consumer_settings=consumer_settings)

asyncio.run(consumer.register_simple_event(topics=kafka_settings.kafka_topic, message_handler=message_handler))
```
