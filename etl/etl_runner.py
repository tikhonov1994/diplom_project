from extractors.person_extractor import PersonExtractor
from extractors.genre_extractor import GenreExtractor
from extractors.movie_extractor import MovieExtractor
from datetime import datetime
import psycopg2
import backoff
from transformer import Transformer
from state import State, JsonFileStorage
from loader import LoadToElastic
from elasticsearch.exceptions import ConnectionError
from dotenv import load_dotenv
from configs import app_config as config

load_dotenv()


class ETL:
    POSTGRES_ES_MAPPING: dict = {
        'film_work': 'movies',
        'genre': 'genres',
        'person': 'persons'
    }

    def __init__(self, es_conn, pg_conn, table_name: str, index_name: str):
        self.pg_conn = pg_conn
        self.table_name = table_name
        self.index_name = index_name
        self.state = State(JsonFileStorage(config.state_storage_name))
        self.loader = LoadToElastic(es_conn, self.state, index_name)
        self.transformer = Transformer(table_name)

    @backoff.on_exception(backoff.expo, (psycopg2.DatabaseError, psycopg2.OperationalError, ConnectionError),
                          max_tries=10)
    def run_movie_process(self):
        for table_name in self.POSTGRES_ES_MAPPING.keys():
            extractor = MovieExtractor(self.pg_conn, table_name)
            state_key = f'movies_by_{table_name}_last_updated'
            last_updated_at = self.state.get_state(state_key) or str(datetime.min)

            loader_coro = self.loader.load(state_key)
            transformer_coro = self.transformer.transform(loader_coro)
            extractor_coro = extractor.produce(extractor.enrich(extractor.merge(transformer_coro)))

            extractor.produce(extractor.enrich(extractor.merge(transformer_coro)))

            extractor_coro.send(last_updated_at)

    @backoff.on_exception(backoff.expo, (psycopg2.DatabaseError, psycopg2.OperationalError, ConnectionError),
                          max_tries=10)
    def run_genre_process(self):
        extractor = GenreExtractor(self.pg_conn, self.table_name)
        state_key = f'{self.table_name}_last_updated'
        last_updated_at = self.state.get_state(state_key) or str(datetime.min)

        loader_coro = self.loader.load(state_key)
        transformer_coro = self.transformer.transform(loader_coro)
        extractor_coro = extractor.produce(transformer_coro)

        extractor_coro.send(last_updated_at)

    @backoff.on_exception(backoff.expo, (psycopg2.DatabaseError, psycopg2.OperationalError, ConnectionError),
                          max_tries=10)
    def run_person_process(self):
        extractor = PersonExtractor(self.pg_conn, self.table_name)
        state_key = f'{self.table_name}_last_updated'
        last_updated_at = self.state.get_state(state_key) or str(datetime.min)

        loader_coro = self.loader.load(state_key)
        transformer_coro = self.transformer.transform(loader_coro)
        extractor_coro = extractor.produce(transformer_coro)

        extractor_coro.send(last_updated_at)
