from typing import Annotated

from fastapi import Depends

from services.role import RoleService
from services.user import UserService
from services.auth import AuthService
from services.exceptions import (ServiceItemNotFound,
                                 ServiceConflictOnAddError,
                                 ServiceConflictOnDeleteError)
from services.utils import UtilService

RoleServiceDep = Annotated[RoleService, Depends()]
UserServiceDep = Annotated[UserService, Depends()]
AuthServiceDep = Annotated[AuthService, Depends()]
UtilServiceDep = Annotated[UtilService, Depends()]

__all__ = ['RoleServiceDep',
           'UserServiceDep',
           'UtilServiceDep',
           'AuthServiceDep',
           'ServiceItemNotFound',
           'ServiceConflictOnAddError',
           'ServiceConflictOnDeleteError']
