from time import sleep
from uuid import uuid4
import pytest
from http import HTTPStatus
from functional.utils.db import get_from_db

from functional.test_data.db_data import test_notification_template, test_notification_register_template

pytestmark = pytest.mark.asyncio

ENDPOINT = '/notification_api/api/v1/mailing/'


async def test_send_mailing(http_notification_client, db_session, add_test_template) -> None:
    template_in_db = await get_from_db(db_session, 'template', ('name', test_notification_template.get('name')),
                                       'notification')
    assert template_in_db is not None

    payload = {'recipients_list': [str(uuid4()), str(uuid4())], 'template_id': str(template_in_db['id']),
               'template_params': {'param': 'value'}, 'subject': 'test_subject'}
    async with http_notification_client.post(f'{ENDPOINT}send',
                                             json=payload) as response:
        assert response.status == HTTPStatus.OK

        sleep(0.2)
        notification_in_db = await get_from_db(db_session, 'mailing', ('template_id', template_in_db['id']),
                                               'notification')
        assert notification_in_db is not None


async def test_send_registration_mailing(http_notification_client, db_session, add_register_template) -> None:
    body = {'user_id': str(uuid4()), 'email': 'test_welcome@mail.com'}
    async with http_notification_client.post(f'{ENDPOINT}welcome_user',
                                             json=body) as response:
        assert response.status == HTTPStatus.OK

        sleep(0.2)
        notification_in_db = await get_from_db(db_session, 'mailing', (
            'template_id', test_notification_register_template['id']
        ), 'notification')
        assert notification_in_db is not None
