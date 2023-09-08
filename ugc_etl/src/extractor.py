import threading
from kafka import KafkaConsumer
from src.core.config import app_config

TOPIC_NAME = 'views'


class Consumer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        consumer = KafkaConsumer(
            bootstrap_servers='localhost:9092',
            # bootstrap_servers=[f'{app_config.kafka_host}:{app_config.kafka_port}'],
            auto_offset_reset='earliest', )
        consumer.subscribe([TOPIC_NAME])

        while not self.stop_event.is_set():
            for message in consumer:
                # print(message)
                yield message
                if self.stop_event.is_set():
                    break

        consumer.close()
