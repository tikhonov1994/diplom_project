from typing import Annotated

from fastapi import Depends

from db.storage.generic_storage import GenericStorage, ItemNotFoundException
from db.model import UserInfo, UserRole, UserSession

UserInfoStorageDep = Annotated[GenericStorage[UserInfo], Depends()]
UserRoleStorageDep = Annotated[GenericStorage[UserRole], Depends()]
UserSessionStorageDep = Annotated[GenericStorage[UserSession], Depends()]

__all__ = ['UserInfoStorageDep',
           'UserRoleStorageDep',
           'UserSessionStorageDep',
           'ItemNotFoundException']
