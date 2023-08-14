import pytest
import time

from aiohttp import ClientSession
from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession

from functional.utils.db import insert_into_db, get_from_db
from functional.test_data.db_data import test_register

REGISTER_ENDPOINT = '/auth/api/v1/auth/register/'
LOGIN_ENDPOINT = '/auth/api/v1/auth/login'
HISTORY_ENDPOINT = '/auth/api/v1/auth/history/'
USER_DATA = {'email': test_register.get('email'), 'password': test_register.get('password')}
pytestmark = pytest.mark.asyncio


async def test_user_registration(http_auth_client: ClientSession, db_session: AsyncSession) -> None:
    assert await get_from_db(db_session, 'user_info', ('email', test_register.get('email')), 'auth') is None
    async with http_auth_client.post(REGISTER_ENDPOINT, json=USER_DATA) as response:
        assert response.status == HTTPStatus.OK
        response_data = await response.json()
        assert response_data.get('access_token') and response_data.get('refresh_token')

    # wait for auth service to commit changes
    time.sleep(0.2)

    user_in_db = await get_from_db(db_session, 'user_info', ('email', test_register.get('email')), 'auth')
    assert user_in_db is not None
    assert user_in_db['email'] == test_register.get('email')


async def test_repeat_registration(http_auth_client: ClientSession, db_session: AsyncSession) -> None:
    assert await get_from_db(db_session, 'user_info', ('email', test_register.get('email')), 'auth') is not None
    async with http_auth_client.post(REGISTER_ENDPOINT, json=USER_DATA) as response:
        assert response.status == HTTPStatus.BAD_REQUEST


async def test_user_history(http_auth_client: ClientSession) -> None:
    async with http_auth_client.post(LOGIN_ENDPOINT, json=USER_DATA) as response:
        assert response.status == HTTPStatus.OK
        response_data = await response.json()
        access_token = response_data.get('access_token')
    headers = {'Authorization': f'Bearer {access_token}'}
    async with http_auth_client.get(HISTORY_ENDPOINT, headers=headers) as response:
        assert response.status == HTTPStatus.OK
        response_data = await response.json()
        assert len(response_data) == 2
