from uuid import uuid4, UUID
from time import sleep

import pytest
from http import HTTPStatus

from functional.test_data.auth_data import test_auth_headers
from functional.test_data.mongo_data import test_movieLikes

pytestmark = pytest.mark.asyncio

ENDPOINT = '/social_api/api/v1/rating/'
RATE_BODY = {'movie_id': str(uuid4()), 'rating_value': 7}


async def test_rate_movie_auth(http_social_client) -> None:
    async with http_social_client.post(f'{ENDPOINT}movie/rate', json=RATE_BODY) as response:
        assert response.status == HTTPStatus.UNAUTHORIZED


async def test_rate_movie(http_social_client, get_data_from_social_db) -> None:
    data_query = {'entity_id': {'$eq': UUID(RATE_BODY['movie_id'])}}
    assert not await get_data_from_social_db('movieLikes', data_query)
    async with http_social_client.post(f'{ENDPOINT}movie/rate', json=RATE_BODY, headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.OK
    sleep(0.2)
    assert await get_data_from_social_db('movieLikes', data_query)

# async def test_rate_not_existing_movie(http_social_client) -> None:
#     ...
#
#
# async def test_like_movie_auth(http_social_client) -> None:
#     ...
#
#
# async def test_like_movie(http_social_client) -> None:
#     ...
#
#
# async def test_like_not_existing_movie(http_social_client) -> None:
#     ...
#
#
# async def test_dislike_movie_auth(http_social_client) -> None:
#     ...
#
#
# async def test_dislike_movie(http_social_client) -> None:
#     ...
#
#
# async def test_dislike_not_existing_movie(http_social_client) -> None:
#     ...
#
#
# async def test_delete_movie_auth(http_social_client) -> None:
#     ...
#
#
# async def test_delete_movie(http_social_client) -> None:
#     ...
#
#
# async def test_delete_not_existing_movie(http_social_client) -> None:
#     ...
#
#
# async def test_get_movie_rating_auth(http_social_client) -> None:
#     ...
#
#
# async def test_get_movie_rating(http_social_client) -> None:
#     ...
#
#
# async def test_get_not_existing_movie_rating(http_social_client) -> None:
#     ...
