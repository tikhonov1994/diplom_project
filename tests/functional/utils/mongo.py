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
    likes_count = dislikes_count = 0
    rating_value = 0.
    for rec in data:
        if rec['value'] == 10:
            likes_count += 1
        if rec['value'] == 0:
            dislikes_count += 1
        rating_value += rec['value']
    rating_value /= len(data)

    return {
        'movie_id': entity_id,
        'likes_count': likes_count,
        'dislikes_count': dislikes_count,
        'rating_value': rating_value
    }
