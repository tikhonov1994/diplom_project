from collections import namedtuple
from uuid import uuid4

from settings import test_settings

PasswordAndHash = namedtuple('PasswordAndHash', 'password hash')

test_password_and_hash_pair = PasswordAndHash('hackme',
                                              r'f59a33e80babb1d53516302590fa7ff123f9ed533a54c'
                                              r'cab565924e84c8d271f46b4902a1a8fe21392e43e6de6c1'
                                              r'c21de91399ca73bdd3bed0b66dc14ec96c00')

test_user_role = {
    'id': str(uuid4()),
    'name': 'test_user_role'
}

test_admin_role = {
    'id': str(uuid4()),
    'name': test_settings.admin_user_role
}

test_user_info = {
    'id': str(uuid4()),
    'email': 'test_user@testservice.com',
    'password_hash': test_password_and_hash_pair.hash,
    'user_role_id': test_user_role['id']
}

test_admin_info = {
    'id': str(uuid4()),
    'email': 'test_admin@testservice.com',
    'password_hash': test_password_and_hash_pair.hash,
    'user_role_id': test_admin_role['id']
}

test_register = {
    'email': 'new_user@testservice.com',
    'password': 'hackme',
}

test_notification_template = {
    'id': str(uuid4()),
    'name': 'test_template',
    'html_template': 'test_html',
    'attributes': {"param1": "value1", "param2": "value2"},
}

test_notification_register_template = {
    'id': str(uuid4()),
    'name': 'registration',
    'html_template': 'test_html',
    'attributes': {"param1": "value1", "param2": "value2"},
}