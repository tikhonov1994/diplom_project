import http
import json
import uuid
from urllib.parse import urlparse
import logging

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

logging.basicConfig(filename='logging.log', level=int(settings.LOGGING_LEVEL),
                    format='%(asctime)s  %(message)s')
logger = logging.getLogger(__name__)


User = get_user_model()


class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        url = settings.AUTH_API_LOGIN_URL
        headers = {'X-Request-Id': str(uuid.uuid4())}
        payload = {'email': username, 'password': password}

        session = requests.Session()
        retries = Retry(total=settings.BACKOFF_RETRIES_COUNT,
                        backoff_factor=1)
        session.mount(urlparse(settings.AUTH_API_LOGIN_URL).scheme,
                      HTTPAdapter(max_retries=retries))

        response = session.post(url, data=json.dumps(payload), headers=headers)
        if response.status_code != http.HTTPStatus.OK:
            return None

        data = response.json()

        try:
            user, _ = User.objects.get_or_create(id=data['user_id'], )
            user.email = data.get('email')
            user.is_admin = data.get('role') == 'admin'
            user.save()
        except Exception as error:
            logger.error(str(error))
            return None

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
