from aiokafka import AIOKafkaProducer
from core.config import app_config


class CustomKafkaProducer:
    def __init__(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=[f'{app_config.kafka_host}:{app_config.kafka_port}'],
        )

    async def send(self, topic: str, key, value):
        await self.producer.start()
        try:
            await self.producer.send_and_wait(
                topic=topic,
                key=key,
                value=value,
            )
        finally:
            await self.producer.stop()


async def get_producer() -> CustomKafkaProducer:
    return CustomKafkaProducer()
