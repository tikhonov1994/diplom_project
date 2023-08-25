import random, string
from yandexid.schemas.yandexid import User
from db.model import UserInfo

from yandexid import AsyncYandexOAuth, AsyncYandexID

from core.config import app_config
from db.storage import (UserInfoStorageDep,
                        UserRoleStorageDep, UserSocialStorageDep)
from services.exceptions import ServiceUniqueFieldViolation
from services.utils import generate_hashed_password

from services.oauth_base import OauthBase


class YandexOauthService(OauthBase):
    def __init__(self, social_storage: UserSocialStorageDep,
                 info_storage: UserInfoStorageDep,
                 role_storage: UserRoleStorageDep) -> None:
        super().__init__(social_storage, info_storage, role_storage)
        self._yandex_oauth = AsyncYandexOAuth(
            client_id=app_config.yandex_client_id,
            client_secret=app_config.yandex_client_secret,
            redirect_uri=app_config.yandex_client_redirect_uri
        )

    async def get_authorization_url(self):
        return self._yandex_oauth.get_authorization_url()

    async def get_user_info(self, code: str):
        token = await self._yandex_oauth.get_token_from_code(code)
        yandex_id = AsyncYandexID(token.access_token)
        user_info = await yandex_id.get_user_info_json()
        return user_info

    async def get_or_create_user(self, user_data: User) -> UserInfo:
        if user_id := await self._social_storage.get_user_by_social_id(user_data.client_id):
            return await self._info_storage.generic.get(user_id)
        email = user_data.default_email
        if await self._info_storage.email_already_taken(email):
            raise ServiceUniqueFieldViolation(item_name='UserInfo',
                                              search_field='email',
                                              search_val=email)
        letters = string.ascii_letters
        password = ''.join(random.choice(letters) for _ in range(15))
        hashed_password = generate_hashed_password(password)
        role = await self._role_storage.get_default_role()
        user = UserInfo(email=email, password_hash=hashed_password,
                        user_role_id=role.id)
        await self._info_storage.add_user(user)
        await self._social_storage.create_user_social(user.id, user_data.client_id)
        return user