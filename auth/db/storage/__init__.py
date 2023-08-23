from typing import Annotated

from core.oauth2 import AuthJWT
from db.storage.generic_storage import (DbConflictException,
                                        ItemNotFoundException)
from db.storage.role_storage import RoleStorage
from db.storage.user_info_storage import (UserEmailNotFoundException,
                                          UserInfoStorage)
from db.storage.user_session_storage import UserSessionStorage
from db.storage.user_social_storage import UserSocialStorage
from fastapi import Depends

UserInfoStorageDep = Annotated[UserInfoStorage, Depends()]
UserRoleStorageDep = Annotated[RoleStorage, Depends()]
UserSessionStorageDep = Annotated[UserSessionStorage, Depends()]
UserSocialStorageDep = Annotated[UserSocialStorage, Depends()]
AuthDep = Annotated[AuthJWT, Depends()]

__all__ = ['UserInfoStorageDep',
           'UserRoleStorageDep',
           'UserSessionStorageDep',
           'AuthDep',
           'ItemNotFoundException',
           'DbConflictException',
           'UserSocialStorageDep',
           'UserEmailNotFoundException']
