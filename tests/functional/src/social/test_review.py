from http import HTTPStatus
from random import randint
from time import sleep
from uuid import UUID, uuid4

import pytest
from functional.test_data.auth_data import test_auth_headers
from functional.test_data.db_data import test_user_info
from functional.test_data.mongo_data import test_reviews_data

pytestmark = pytest.mark.asyncio

ENDPOINT = '/social_api/api/v1/reviews/'


def _get_review_body(film_id: UUID | None = None) -> dict[str, any]:
    return {'film_id': str(film_id) if film_id else str(uuid4()),
            'author_rating': randint(0, 10), 'text': 'Test text'}


async def test_add_review_auth(http_social_client) -> None:
    async with http_social_client.post(f'{ENDPOINT}add',
                                       json=_get_review_body()) as response:
        assert response.status == HTTPStatus.UNAUTHORIZED


async def test_review_add(http_social_client, get_data_from_social_db) -> None:
    review_body = _get_review_body()
    data_query = {'film_id': {'$eq': UUID(review_body['film_id'])}}
    assert not await get_data_from_social_db('reviews', data_query)

    async with http_social_client.post(f'{ENDPOINT}add',
                                       json=review_body,
                                       headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.OK

    sleep(0.2)
    review_data = await get_data_from_social_db('reviews', data_query)
    assert review_data
    assert review_data[0].get('author_rating') == review_body.get('author_rating')


async def test_like_dislike_review(http_social_client, get_data_from_social_db) -> None:
    review_id_to_like = test_reviews_data[0].get('review_id')
    like_query = {'$and': [
        {'user_id': {'$eq': UUID(test_user_info.get('id'))}},
        {'review_id': {'$eq': review_id_to_like}}
    ]}
    assert not await get_data_from_social_db('review_assessments', like_query)

    async with http_social_client.post(f'{ENDPOINT}{str(review_id_to_like)}/assessment/like',
                                       headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.OK

    sleep(0.2)
    like_data = await get_data_from_social_db('review_assessments', like_query)
    assert like_data
    assert like_data[0].get('liked') is True

    async with http_social_client.post(f'{ENDPOINT}{str(review_id_to_like)}/assessment/dislike',
                                       headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.OK

    sleep(0.2)
    like_data = await get_data_from_social_db('review_assessments', like_query)
    assert like_data
    assert like_data[0].get('liked') is False

    async with http_social_client.delete(f'{ENDPOINT}{str(review_id_to_like)}/assessment/delete',
                                         headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.OK

    sleep(0.2)
    like_data = await get_data_from_social_db('review_assessments', like_query)
    assert not like_data


async def test_rating_reviw(http_social_client, get_data_from_social_db) -> None:
    review_id = test_reviews_data[0].get('review_id')
    query = {'review_id': {'$eq': review_id}}
    data = await get_data_from_social_db('review_assessments', query)
    like_count, dislike_count = 0, 0
    for i in data:
        if i.get('liked') is True:
            like_count += 1
        else:
            dislike_count += 1
    
    async with http_social_client.get(f'{ENDPOINT}{str(review_id)}/assessment',
                                      headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.OK
        data = await response.json()
        assert data.get('likes_count') == like_count
        assert data.get('dislikes_count') == dislike_count


async def test_sort_filter_review(http_social_client, get_data_from_social_db) -> None:
    query = {'author_rating': {'$lte': 5}}
    db_data = await get_data_from_social_db('reviews', query)
    async with http_social_client.get(f'{ENDPOINT}?order=added_asc&filter_field=author_rating&filter_argument=lte&rating_value=5',
                                      headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.OK
        data = await response.json()
        assert len(data) == len(db_data)
        for i in range(len(data)):
            if i > 0:
                assert data[i].get('added') > data[i-1].get('added')
