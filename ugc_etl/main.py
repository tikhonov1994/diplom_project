from src.extractor import Consumer


def run_etl():
    kafka_consumer = Consumer()

    messages = []
    for message in kafka_consumer.run():
        print(message)
        messages.append(message)


if __name__ == '__main__':
    run_etl()
