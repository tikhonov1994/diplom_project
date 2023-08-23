import http
import json
import os
import uuid

import requests
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        url = os.environ.get('AUTH_API_LOGIN_URL')
        headers = {'X-Request-Id': str(uuid.uuid4())}

        payload = {'email': username, 'password': password}
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        if response.status_code != http.HTTPStatus.OK:
            return None

        data = response.json()

        try:
            user, created = User.objects.get_or_create(id=data['user_id'], )
            user.email = data.get('email')
            user.is_admin = data.get('role') == 'admin'
            user.save()
        except Exception:
            return None

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None