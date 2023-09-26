import logging
import psycopg2
from typing import Generator

from configs import app_config as config
from decorators import coroutine
from extractors.base_extractor import BaseExtractor
from logger import logger


class GenreExtractor(BaseExtractor):
    table_name = 'genre'

    @coroutine
    def produce(self, transformer: Generator) -> Generator:
        logger.info(f"Extracting table '{self.table_name}'")
        with self.connection.cursor() as curs:
            while last_updated := (yield):
                query = f"""SELECT id, name, updated_at 
                        FROM content.{self.table_name} 
                        WHERE updated_at > '{last_updated}'
                        ORDER BY updated_at"""
                curs.execute(query)
                try:
                    while data := curs.fetchmany(size=self.BATCH_SIZE):
                        last_updated = data[-1][-1]
                        transformer.send((data, last_updated))
                except psycopg2.Error as error:
                    logger.error('Error while extracting data from table %s. Error: %s', self.table_name, error)
