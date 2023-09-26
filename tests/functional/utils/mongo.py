from uuid import UUID

from pymongo import MongoClient


def drop_collection(client: MongoClient,
                    db_name: str,
                    collection_name: str) -> None:
    client[db_name].drop_collection(collection_name)


def insert_data_to_collection(client: MongoClient,
                              db_name: str,
                              collection_name: str,
                              data: list[dict[str, any]]) -> None:
    client[db_name][collection_name].insert_many(data)


def calc_rating_for_entity(entity_id: UUID,
                           data: list[dict[str, any]]) -> dict[str, any] | None:
    ...
