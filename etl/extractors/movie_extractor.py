import logging
import psycopg2
from typing import Generator
from decorators import coroutine
from configs import app_config as config
from extractors.base_extractor import BaseExtractor
from logger import logger


class MovieExtractor(BaseExtractor):
    @coroutine
    def produce(self, enricher: Generator) -> Generator:
        logger.info("Extractor started processing...")
        logger.info(f"Extracting table '{self.table_name}'")
        with self.connection.cursor() as curs:
            while last_updated := (yield):
                query = f"SELECT id, updated_at FROM content.{self.table_name} WHERE updated_at > '{last_updated}' ORDER BY updated_at"
                curs.execute(query)
                try:
                    while data := curs.fetchmany(size=self.BATCH_SIZE):
                        last_updated = data[-1][1]
                        enricher.send((data, last_updated))
                except psycopg2.Error as error:
                    logger.error('Error while extracting data from table %s. Error: %s', self.table_name, error)

    @coroutine
    def enrich(self, merger: Generator) -> Generator:
        with self.connection.cursor() as curs:
            while True:
                data, last_updated = (yield)
                if self.table_name != 'film_work':
                    batch_ids = "'" + "', '".join([data[0] for data in data]) + "'"
                    related_table = f'{self.table_name}_film_work'
                    query = f"""
                        SELECT fw.id, fw.updated_at
                        FROM content.film_work fw
                        LEFT JOIN content.{related_table} as related_table ON related_table.film_work_id = fw.id
                        WHERE related_table.{self.table_name}_id::text IN ({batch_ids})
                        ORDER BY fw.updated_at;
                    """

                    try:
                        curs.execute(query)
                        while result := curs.fetchmany(size=self.BATCH_SIZE):
                            merger.send((result, last_updated))
                        continue
                    except psycopg2.Error as error:
                        logger.error('Error while enriching data from table %s to index movies. Error: %s', self.table_name, error)
                merger.send((data, last_updated))

    @coroutine
    def merge(self, transformer: Generator) -> Generator:
        with self.connection.cursor() as curs:
            while True:
                data, last_updated = (yield)
                batch_ids = "'" + "', '".join([data[0] for data in data]) + "'"
                query = f"""
                    SELECT
                        fw.id,
                        fw.rating as imdb_rating,
                        fw.title,
                        fw.description,
                        COALESCE(json_agg(DISTINCT jsonb_build_object('id', g.id, 'name', g.name)), '[]') AS genre,
                        ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'director') AS directors,
                        COALESCE(json_agg(DISTINCT jsonb_build_object('id', p.id, 'full_name', p.full_name)) FILTER (WHERE pfw.role = 'director'), '[]') AS directors,
                        COALESCE(json_agg(DISTINCT jsonb_build_object('id', p.id, 'full_name', p.full_name)) FILTER (WHERE pfw.role = 'actor'), '[]') AS actors,
                        COALESCE(json_agg(DISTINCT jsonb_build_object('id', p.id, 'full_name', p.full_name)) FILTER (WHERE pfw.role = 'writer'), '[]') AS writers
                    FROM content.film_work fw
                    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                    LEFT JOIN content.person p ON p.id = pfw.person_id
                    LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                    LEFT JOIN content.genre g ON g.id = gfw.genre_id
                    WHERE fw.id::text IN ({batch_ids})
                    GROUP BY fw.id
                    ORDER BY fw.updated_at
                """

                try:
                    curs.execute(query)
                    while result := curs.fetchmany(size=self.BATCH_SIZE):
                        transformer.send((result, last_updated))
                except psycopg2.Error as error:
                    logger.error('Error while merging data from table %s. Error: %s', self.table_name, error)
