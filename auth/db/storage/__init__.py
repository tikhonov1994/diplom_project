from typing import Annotated

from fastapi import Depends

from db.storage.generic_storage import ItemNotFoundException, DbConflictException
from db.storage.user_info_storage import UserInfoStorage
from db.storage.role_storage import RoleStorage

UserInfoStorageDep = Annotated[UserInfoStorage, Depends()]
UserRoleStorageDep = Annotated[RoleStorage, Depends()]

__all__ = ['UserInfoStorageDep',
           'UserRoleStorageDep',
           'ItemNotFoundException',
           'DbConflictException']
