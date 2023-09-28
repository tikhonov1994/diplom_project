from elasticsearch import Elasticsearch, helpers
from decorators import coroutine
from state import State
from logger import logger


class LoadToElastic:
    def __init__(self, es: Elasticsearch, state: State, index_name: str):
        self.es = es
        self.state = state
        self.index_name = index_name

    @coroutine
    def load(self, state_key: str):
        while True:
            data, last_updated = (yield)
            actions = [{'_index': self.index_name, '_id': row.id, '_source': row.json()} for row in data]
            rows_count, errors = helpers.bulk(self.es, actions)

            self.state.set_state(state_key, str(last_updated))
            if errors:
                logger.error('Error while loading data to elasticsearch. Error: %s', errors)

            logger.info(f'Loaded {rows_count} entries to elasticsearch')
