from datetime import datetime
from random import randint
from time import sleep
from uuid import uuid4, UUID

import pytest
from http import HTTPStatus

from functional.test_data.auth_data import test_auth_headers
from functional.test_data.db_data import test_user_info
from functional.test_data.mongo_data import test_movieLikes
from functional.utils.mongo import calc_rating_for_entity

pytestmark = pytest.mark.asyncio

ENDPOINT = '/social_api/api/v1/rating/'


def _get_rate_body(entity_id: UUID | None = None) -> dict[str, any]:
    return {'movie_id': str(entity_id) if entity_id else str(uuid4()), 'rating_value': randint(0, 10)}


async def test_rate_movie_auth(http_social_client) -> None:
    async with http_social_client.post(f'{ENDPOINT}movie/rate',
                                       json=_get_rate_body()) as response:
        assert response.status == HTTPStatus.UNAUTHORIZED


async def test_rate_movie(http_social_client, get_data_from_social_db) -> None:
    rate_body = _get_rate_body()
    data_query = {'entity_id': {'$eq': UUID(rate_body['movie_id'])}}
    assert not await get_data_from_social_db('movieLikes', data_query)

    async with http_social_client.post(f'{ENDPOINT}movie/rate',
                                       json=rate_body,
                                       headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.OK

    sleep(0.2)
    rate_data = await get_data_from_social_db('movieLikes', data_query)
    assert rate_data
    assert rate_data[0].get('value') == rate_body.get('rating_value')


async def test_like_movie_auth(http_social_client) -> None:
    async with http_social_client.post(f'{ENDPOINT}movie/{str(uuid4())}/like') as response:
        assert response.status == HTTPStatus.UNAUTHORIZED


async def test_like_movie(http_social_client, get_data_from_social_db) -> None:
    movie_id_to_like = uuid4()
    like_query = {'entity_id': {'$eq': movie_id_to_like}}
    assert not await get_data_from_social_db('movieLikes', like_query)

    async with http_social_client.post(f'{ENDPOINT}movie/{str(movie_id_to_like)}/like',
                                       headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.OK

    sleep(0.2)
    like_data = await get_data_from_social_db('movieLikes', like_query)
    assert like_data
    assert like_data[0].get('value') == 10


async def test_dislike_movie_auth(http_social_client) -> None:
    async with http_social_client.post(f'{ENDPOINT}movie/{str(uuid4())}/dislike') as response:
        assert response.status == HTTPStatus.UNAUTHORIZED


async def test_dislike_movie(http_social_client, get_data_from_social_db) -> None:
    movie_id_to_dislike = uuid4()
    dislike_query = {'entity_id': {'$eq': movie_id_to_dislike}}
    assert not await get_data_from_social_db('movieLikes', dislike_query)

    async with http_social_client.post(f'{ENDPOINT}movie/{str(movie_id_to_dislike)}/dislike',
                                       headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.OK

    sleep(0.2)
    dislike_data = await get_data_from_social_db('movieLikes', dislike_query)
    assert dislike_data
    assert dislike_data[0].get('value') == 0


async def test_delete_movie_auth(http_social_client) -> None:
    async with http_social_client.delete(f'{ENDPOINT}movie/{str(uuid4())}/rate') as response:
        assert response.status == HTTPStatus.UNAUTHORIZED


async def test_delete_movie(http_social_client, add_data_to_social_db, get_data_from_social_db) -> None:
    movie_to_delete_id = uuid4()
    rating_data = [{
        'user_id': UUID(test_user_info.get('id')),
        'entity_id': movie_to_delete_id,
        'value': 5,
        'added': datetime.now()
    }]
    await add_data_to_social_db('movieLikes', rating_data)
    assert await get_data_from_social_db('movieLikes', {'$and': [
        {'entity_id': movie_to_delete_id},
        {'user_id': UUID(test_user_info.get('id'))}
    ]})

    async with http_social_client.delete(f'{ENDPOINT}movie/{str(movie_to_delete_id)}/rate',
                                         headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.OK

    sleep(0.2)
    assert not await get_data_from_social_db('movieLikes', {'$and': [
        {'entity_id': movie_to_delete_id},
        {'user_id': UUID(test_user_info.get('id'))}
    ]})


async def test_delete_not_existing_movie(http_social_client) -> None:
    async with http_social_client.delete(f'{ENDPOINT}movie/{str(uuid4())}/rate',
                                         headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.NOT_FOUND


async def test_get_movie_rating_auth(http_social_client) -> None:
    async with http_social_client.get(f'{ENDPOINT}movie/{str(uuid4())}') as response:
        assert response.status == HTTPStatus.UNAUTHORIZED


async def test_get_movie_rating(http_social_client) -> None:
    entity_id = test_movieLikes[0].get('entity_id')
    rating = calc_rating_for_entity(entity_id, test_movieLikes)

    async with http_social_client.get(f'{ENDPOINT}movie/{str(entity_id)}',
                                      headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.OK
        data = await response.json()
        assert str(rating['movie_id']) == data['movie_id']
        assert rating['likes_count'] == data['likes_count']
        assert rating['dislikes_count'] == data['dislikes_count']
        assert rating['rating_value'] == data['rating_value']


async def test_get_not_existing_movie_rating(http_social_client) -> None:
    async with http_social_client.get(f'{ENDPOINT}movie/{str(uuid4())}',
                                      headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.NOT_FOUND
