import time
from http import HTTPStatus
import pytest
from aiohttp.client import ClientSession

from functional.test_data.auth_data import test_create_profile_auth_headers, test_auth_headers
from functional.test_data.user_data import test_user_profile_create, test_user_profile
from functional.utils.db import get_from_db

BASE_ENDPOINT = '/user_api/api/v1/profile/'

pytestmark = pytest.mark.asyncio


async def test_add_profile_auth(http_user_client: ClientSession) -> None:
    async with http_user_client.post(f'{BASE_ENDPOINT}create',
                                     json=test_user_profile_create) as response:
        assert response.status == HTTPStatus.UNAUTHORIZED


async def test_add_profile(http_user_client: ClientSession, secure_db_session) -> None:
    assert await get_from_db(secure_db_session, 'user_profile', ('name', test_user_profile_create['name']), 'public') \
           is None

    async with http_user_client.post(f'{BASE_ENDPOINT}create',
                                     json=test_user_profile_create,
                                     headers=test_create_profile_auth_headers) as response:
        assert response.status == HTTPStatus.OK

    time.sleep(0.2)

    assert await get_from_db(secure_db_session, 'user_profile',
                             ('name', test_user_profile_create['name']), 'public') is not None


async def test_update_profile_auth(http_user_client: ClientSession) -> None:
    body = {'name': 'new_name'}
    async with http_user_client.patch(f'{BASE_ENDPOINT}update',
                                      json=body) as response:
        assert response.status == HTTPStatus.UNAUTHORIZED


async def test_update_profile(http_user_client: ClientSession, secure_db_session) -> None:
    assert await get_from_db(secure_db_session, 'user_profile', ('name', test_user_profile['name']), 'public') \
           is not None

    body = {'name': 'new_name'}
    async with http_user_client.patch(f'{BASE_ENDPOINT}update',
                                      json=body,
                                      headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.OK

    time.sleep(0.2)

    assert await get_from_db(secure_db_session, 'user_profile',
                             ('name', test_user_profile['name']), 'public') is not None


async def test_get_profile_auth(http_user_client: ClientSession) -> None:
    async with http_user_client.get(f'{BASE_ENDPOINT}get') as response:
        assert response.status == HTTPStatus.UNAUTHORIZED


async def test_get_profile(http_user_client: ClientSession, secure_db_session) -> None:
    db_data = await get_from_db(secure_db_session, 'user_profile', ('name', test_user_profile['name']), 'public')

    async with http_user_client.get(f'{BASE_ENDPOINT}get',
                                    headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.OK

        time.sleep(0.2)

        data = await response.json()
        assert data.get('name') == db_data['name']


async def test_delete_profile_auth(http_user_client: ClientSession) -> None:
    async with http_user_client.delete(f'{BASE_ENDPOINT}delete') as response:
        assert response.status == HTTPStatus.UNAUTHORIZED


async def test_delete_profile(http_user_client: ClientSession, secure_db_session) -> None:
    assert get_from_db(secure_db_session, 'user_profile', ('name', test_user_profile['name']), 'public') is not None

    async with http_user_client.delete(f'{BASE_ENDPOINT}delete',
                                       headers=test_auth_headers) as response:
        assert response.status == HTTPStatus.OK

    time.sleep(0.2)

    assert get_from_db(secure_db_session, 'user_profile', ('name', test_user_profile['name']), 'public') is None
