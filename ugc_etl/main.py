import time
from src.extractor import KafkaConsumer

def run_etl():
    kafka_consumer = KafkaConsumer()

    messages = []
    for message in kafka_consumer.run():
        print(message)
        messages.append(message)


if __name__ == '__main__':
    run_etl()
