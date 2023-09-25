import logging
import os

from elasticsearch import Elasticsearch

from indices import settings, mappings

# noinspection HttpUrlsUsage
es = Elasticsearch(
    hosts=f'http://{os.environ.get("ELASTIC_HOST")}:{os.environ.get("ELASTIC_PORT")}'
)

for idx_name, mapping in mappings.items():
    logging.info('Start migrating Elasticsearch:')
    if not es.indices.exists(index=idx_name):
        logging.info('Adding index \'%s\'..', idx_name)
        es.indices.create(index=idx_name, settings=settings, mappings=mapping)
    logging.info('Elasticsearch migrations have been applied successfully!')
