from src.extractor import KafkaViewsConsumer
from src.transformer import ViewsMessageTransformer as Transformer
from src.loader import ClickhouseViewsLoader


# TODO: REMOVE PRODUCER:
# from kafka import KafkaProducer
# from time import sleep
#
#
# producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
#
# producer.send(
#     topic='views',
#     value=b'1611039931',
#     key=b'dbe578d8-f34c-44f7-81c7-6b59034c8df3+8e5de1f2-5c8f-4dc9-9449-5addbc32a279',
# )
# TODO: END OF TODO


def run_etl():
    consumer = KafkaViewsConsumer()
    loader = ClickhouseViewsLoader()

    for record in consumer.run():
        msg = Transformer.transform(record.key, record.value, record.timestamp)
        print(msg)
        loader.add_message(msg)


if __name__ == '__main__':
    run_etl()
