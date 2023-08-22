from typing import Annotated

from fastapi import Depends
from services.auth import AuthService
from services.exceptions import (ServiceConflictOnAddError,
                                 ServiceConflictOnDeleteError,
                                 ServiceItemNotFound,
                                 ServiceItemSearchException,
                                 ServiceUniqueFieldViolation)
from services.role import RoleService
from services.user import UserService
from services.yandex_oauth import YandexOauthService

RoleServiceDep = Annotated[RoleService, Depends()]
UserServiceDep = Annotated[UserService, Depends()]
AuthServiceDep = Annotated[AuthService, Depends()]
YandexOauthDep = Annotated[YandexOauthService, Depends()]

__all__ = ['RoleServiceDep',
           'UserServiceDep',
           'AuthServiceDep',
           'ServiceItemNotFound',
           'ServiceConflictOnAddError',
           'ServiceConflictOnDeleteError',
           'ServiceUniqueFieldViolation',
           'YandexOauthDep',
           'ServiceItemSearchException']
