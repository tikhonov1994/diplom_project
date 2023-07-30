import logging
import psycopg2
from typing import Generator
from decorators import coroutine
from configs import app_config as config
from extractors.base_extractor import BaseExtractor

logging.basicConfig(filename=config.log_filename, level=config.logging_level,
                    format='%(asctime)s  %(message)s')
logger = logging.getLogger(__name__)


class PersonExtractor(BaseExtractor):
    @coroutine
    def produce(self, transformer: Generator) -> Generator:
        logger.info("Extractor started processing...")
        logger.info(f"Extracting table '{self.table_name}'")
        with self.connection.cursor() as curs:
            while last_updated := (yield):
                query = f"""SELECT 
                            person.id, 
                            person.full_name,
                            COALESCE(json_agg(DISTINCT jsonb_build_object('id', film_work.id, 'role', person_film_work.role)), '[]') AS films,
                            person.updated_at
                        FROM content.{self.table_name} 
                        LEFT JOIN content.person_film_work ON person_film_work.person_id = person.id
                        LEFT JOIN content.film_work ON person_film_work.film_work_id = film_work.id
                        WHERE person.updated_at > '{last_updated}' 
                        GROUP BY person.id
                        ORDER BY person.updated_at"""
                try:
                    curs.execute(query)
                    while data := curs.fetchmany(size=self.BATCH_SIZE):
                        last_updated = data[-1][-1]
                        transformer.send((data, last_updated))
                except psycopg2.Error as error:
                    logger.error('Error while extracting data from table %s. Error: %s', self.table_name, error)
