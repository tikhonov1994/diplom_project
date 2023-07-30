from decorators import coroutine
from typing import Generator
from models import map_models, Person


class Transformer:
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.model = map_models[table_name]

    @coroutine
    def transform(self, loader: Generator) -> Generator[list[dict], None, None]:
        while True:
            data, last_updated = (yield)
            batch = []
            for row in data:
                item = self.model(**row)
                if self.table_name == 'person':
                    item = self.transform_person_films(item)

                batch.append(item)
            loader.send((batch, last_updated))

    @staticmethod
    def transform_person_films(person: Person):
        result = []
        for film in person.films:
            entry_exists = False

            for i in range(len(result)):
                if result[i]['id'] == film['id']:
                    result[i]['roles'].append(film['role'])
                    entry_exists = True
            if not entry_exists:
                result.append({
                    'id': film['id'],
                    'roles': [film['role']],
                })
        person.films = result

        return person
