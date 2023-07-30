import logging
import time

from elasticsearch import Elasticsearch
from redis import Redis

from settings import test_settings as settings


def wait_for(client: any) -> None:
    logging.info('Waiting for \'%s\'..', client.__class__.__name__)
    while True:
        if client.ping():
            logging.info('\'%s\' is available!', client.__class__.__name__)
            break
        time.sleep(1)


if __name__ == '__main__':
    # noinspection HttpUrlsUsage
    elastic_client = Elasticsearch(
        hosts=f'http://{settings.elastic_host}:{settings.elastic_port}',
        verify_certs=False
    )
    wait_for(elastic_client)
    redis_client = Redis(host=settings.redis_host, port=settings.redis_port, ssl=False)
    wait_for(redis_client)
