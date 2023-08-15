from datetime import datetime, timedelta

from jose import jwt

from settings import test_settings
from functional.test_data.db_data import test_user_info

test_claims = {
    'exp': (datetime.now() + timedelta(hours=1)).timestamp(),
    'sub': test_user_info['id'],
    'email': test_user_info['email'],
    'role': 'test_user_role',
    'user_agent': 'test_user_agent',
    'type': 'access'
}

test_access_token = jwt.encode(claims=test_claims,
                               key=test_settings.jwt_secret_key,
                               algorithm=test_settings.jwt_algorithm)

test_auth_headers = {'Authorization': f'Bearer {test_access_token}'}
