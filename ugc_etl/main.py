from src.extractor import KafkaViewsConsumer
from src.transformer import ViewsMessageTransformer as Transformer
from src.loader import ClickhouseViewsLoader
from src.core.logger import logger


def run_etl():
    logger.info('ETL process started')
    consumer = KafkaViewsConsumer()
    loader = ClickhouseViewsLoader()

    for record in consumer.run():
        msg = Transformer.transform(record.key, record.value, record.timestamp)
        loader.add_message(msg)


if __name__ == '__main__':
    run_etl()
