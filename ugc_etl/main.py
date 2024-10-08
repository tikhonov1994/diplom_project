from sentry_sdk import capture_exception

from src.extractor import KafkaViewsConsumer
from src.transformer import ViewsMessageTransformer as Transformer
from src.loader import ClickhouseViewsLoader
from src.core.logger import logger


def run_etl():
    logger.info('ETL process started')
    consumer = KafkaViewsConsumer()
    loader = ClickhouseViewsLoader()

    for record in consumer.run():
        try:
            msg = Transformer.transform(record.key, record.value, record.timestamp)
            loader.add_message(msg)
        except Exception as e:
            capture_exception(e)


if __name__ == '__main__':
    run_etl()
