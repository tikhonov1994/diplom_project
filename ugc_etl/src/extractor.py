import threading
from typing import Generator

from kafka import KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.consumer.fetcher import ConsumerRecord
from src.core.config import app_config
from src.core.logger import logger

_BACKOFF_SETTINGS = {'retry_backoff_ms': 100,
                     'reconnect_backoff_ms': 100,
                     'reconnect_backoff_max_ms': 3000}


class KafkaViewsConsumer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self._bootstrap_servers = [f'{app_config.kafka.host}:{app_config.kafka.port}']

    def migrate(self):
        admin_client = KafkaAdminClient(bootstrap_servers=self._bootstrap_servers,
                                        client_id='views_admin_client',
                                        **_BACKOFF_SETTINGS)
        topic_to_add = NewTopic(name=app_config.topic_name,
                                num_partitions=app_config.topic_partitions_count,
                                replication_factor=app_config.topic_replica_factor)
        admin_client.create_topics(new_topics=[topic_to_add], validate_only=False)

    def stop(self):
        self.stop_event.set()

    def run(self) -> Generator[ConsumerRecord, None, None]:
        try:
            consumer = KafkaConsumer(
                bootstrap_servers=self._bootstrap_servers,
                auto_offset_reset='earliest',
                group_id=app_config.group_id,
                **_BACKOFF_SETTINGS
            )

            if app_config.topic_name not in consumer.topics():
                self.migrate()

            consumer.subscribe([app_config.topic_name])

            while not self.stop_event.is_set():
                for record in consumer:
                    yield record
                    consumer.commit()
                    if self.stop_event.is_set():
                        break

            consumer.close()
        except Exception as exc:
            logger.warning('Failed to connect to kafka: %s', str(exc))
