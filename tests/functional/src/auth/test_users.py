import time
from http import HTTPStatus
from uuid import uuid4

import pytest
from aiohttp import ClientSession
from functional.test_data.auth_data import (test_login_negative_credentials,
                                            test_refresh_credentials)
from functional.test_data.db_data import test_register
from functional.utils.db import get_from_db
from sqlalchemy.ext.asyncio import AsyncSession

REGISTER_ENDPOINT = '/auth/api/v1/auth/register/'
LOGIN_ENDPOINT = '/auth/api/v1/auth/login/'
REFRESH_ENDPOINT = '/auth/api/v1/auth/refresh/'
HISTORY_ENDPOINT = '/auth/api/v1/auth/history/'
LOGOUT_ENDPOINT = '/auth/api/v1/auth/logout/'
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
    headers = await get_headers(http_auth_client)
    async with http_auth_client.get(HISTORY_ENDPOINT, headers=headers) as response:
        assert response.status == HTTPStatus.OK
        response_data = await response.json()
        assert len(response_data) == 2


async def test_logout(http_auth_client: ClientSession) -> None:
    headers = await get_headers(http_auth_client)
    async with http_auth_client.delete(LOGOUT_ENDPOINT, headers=headers) as response:
        assert response.status == HTTPStatus.RESET_CONTENT
    async with http_auth_client.get(HISTORY_ENDPOINT, headers=headers) as response:
        assert response.status == HTTPStatus.UNAUTHORIZED


async def test_login(http_auth_client: ClientSession) -> None:
    async with http_auth_client.post(LOGIN_ENDPOINT, json=USER_DATA) as response:
        assert response.status == HTTPStatus.OK

        response_data = await response.json()
        access_token = response_data.get('access_token')
        refresh_token = response_data.get('access_token')
        assert access_token is not None
        assert refresh_token is not None


async def test_login_negative(http_auth_client: ClientSession, db_session: AsyncSession) -> None:
    assert await get_from_db(db_session, 'user_info', ('email', test_login_negative_credentials['email']), 'auth') is None

    async with http_auth_client.post(LOGIN_ENDPOINT, json=test_login_negative_credentials) as response:
        assert response.status == HTTPStatus.UNAUTHORIZED


async def test_refresh(http_auth_client: ClientSession) -> None:
    async with http_auth_client.post(REGISTER_ENDPOINT, json=test_refresh_credentials) as register_response:
        assert register_response.status == HTTPStatus.OK
        register_response_data = await register_response.json()
        refresh_token = register_response_data.get('refresh_token')

        async with http_auth_client.post(REFRESH_ENDPOINT, json={'refresh_token': refresh_token}) as response:
            assert response.status == HTTPStatus.OK

            response_data = await response.json()
            access_token = response_data.get('access_token')
            refresh_token = response_data.get('access_token')
            assert access_token is not None
            assert refresh_token is not None


async def test_refresh_negative(http_auth_client: ClientSession) -> None:
    async with http_auth_client.post(REFRESH_ENDPOINT, json={'refresh_token': str(uuid4())}) as response:
        assert response.status == HTTPStatus.BAD_REQUEST


async def get_headers(http_auth_client: ClientSession):
    async with http_auth_client.post(LOGIN_ENDPOINT, json=USER_DATA) as response:
        assert response.status == HTTPStatus.OK
        response_data = await response.json()
        access_token = response_data.get('access_token')
    return {'Authorization': f'Bearer {access_token}'}
