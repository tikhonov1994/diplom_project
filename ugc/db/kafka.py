from kafka import KafkaProducer
from core.config import app_config


class CustomKafkaProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=[f'{app_config.kafka_host}:{app_config.kafka_port}'],
        )

    async def send(self, topic: str, key, value):
        self.producer.send(
            topic=topic,
            key=key,
            value=value,
        )


async def get_producer() -> CustomKafkaProducer:
    return CustomKafkaProducer()
