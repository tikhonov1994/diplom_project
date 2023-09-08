import threading
from typing import Generator

from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord
from src.core.config import app_config


class Consumer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self) -> Generator[ConsumerRecord, None, None]:
        consumer = KafkaConsumer(
            bootstrap_servers=[f'{app_config.kafka.host}:{app_config.kafka.port}'],
            auto_offset_reset='earliest', group_id=app_config.group_id)
        consumer.subscribe([app_config.topic_name])

        while not self.stop_event.is_set():
            for record in consumer:
                yield record
                consumer.commit()
                if self.stop_event.is_set():
                    break

        consumer.close()
