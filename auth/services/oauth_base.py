from abc import ABC, abstractmethod
from uuid import UUID

from db.storage import (UserInfoStorageDep,
                        UserRoleStorageDep, UserSocialStorageDep)



class OauthBase(ABC):
    def __init__(self, social_storage: UserSocialStorageDep,
                 info_storage: UserInfoStorageDep,
                 role_storage: UserRoleStorageDep) -> None:
        self._social_storage = social_storage
        self._info_storage = info_storage
        self._role_storage = role_storage

    async def delete_user_social(self, user_id: UUID):
        await self._social_storage.delete_user_social(user_id)

    @abstractmethod
    async def get_authorization_url(self):
        pass

    @abstractmethod
    async def get_user_info(self):
        pass

    @abstractmethod
    async def get_or_create_user(self):
        pass
