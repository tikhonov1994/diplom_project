from datetime import datetime, timedelta
from uuid import uuid4

from functional.test_data.db_data import test_user_info, test_admin_info, test_admin_role
from jose import jwt
from settings import test_settings

test_claims = {
    'exp': (datetime.now() + timedelta(hours=1)).timestamp(),
    'sub': test_user_info['id'],
    'email': test_user_info['email'],
    'role': 'test_user_role',
    'user_agent': 'test_user_agent',
    'type': 'access',
    'jti': str(uuid4())
}

test_access_token = jwt.encode(claims=test_claims,
                               key=test_settings.jwt_secret_key,
                               algorithm=test_settings.jwt_algorithm)

test_admin_claims = {
    'exp': (datetime.now() + timedelta(hours=1)).timestamp(),
    'sub': test_admin_info['id'],
    'email': test_admin_info['email'],
    'role': test_admin_role['name'],
    'user_agent': 'test_user_agent',
    'type': 'access',
    'jti': str(uuid4())
}

test_admin_access_token = jwt.encode(claims=test_admin_claims,
                                     key=test_settings.jwt_secret_key,
                                     algorithm=test_settings.jwt_algorithm)

test_request_id_header = {'X-Request-Id': str(uuid4())}
test_auth_headers = {'Authorization': f'Bearer {test_access_token}'}
test_admin_auth_headers = {'Authorization': f'Bearer {test_admin_access_token}'}

test_refresh_credentials = {
    'email': 'test_refresh@mail.com',
    'password': 'refresh_password',
}

test_login_negative_credentials = {
    'email': 'invalid_email@mail.com',
    'password': 'some_password',
}
