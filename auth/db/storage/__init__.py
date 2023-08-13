from typing import Annotated

from fastapi import Depends

from db.storage.generic_storage import ItemNotFoundException, DbConflictException
from db.storage.user_info_storage import UserInfoStorage
from db.storage.user_session_storage import UserSessionStorage
from db.storage.role_storage import RoleStorage
from core.oauth2 import AuthJWT
from db.redis import redis

UserInfoStorageDep = Annotated[UserInfoStorage, Depends()]
UserRoleStorageDep = Annotated[RoleStorage, Depends()]
UserSessionStorageDep = Annotated[UserSessionStorage, Depends()]
AuthDep = Annotated[AuthJWT, Depends()]
RedisDep = Annotated[redis, Depends()]

__all__ = ['UserInfoStorageDep',
           'UserRoleStorageDep',
           'UserSessionStorageDep',
           'AuthDep',
           'RedisDep',
           'ItemNotFoundException',
           'DbConflictException']
