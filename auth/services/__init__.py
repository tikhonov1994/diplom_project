from typing import Annotated

from fastapi import Depends

from services.role import RoleService
from services.user import UserService
from services.auth import AuthService
from services.exceptions import (ServiceItemNotFound,
                                 ServiceConflictOnAddError,
                                 ServiceConflictOnDeleteError)

RoleServiceDep = Annotated[RoleService, Depends()]
UserServiceDep = Annotated[UserService, Depends()]
AuthServiceDep = Annotated[AuthService, Depends()]

__all__ = ['RoleServiceDep',
           'UserServiceDep',
           'AuthServiceDep',
           'ServiceItemNotFound',
           'ServiceConflictOnAddError',
           'ServiceConflictOnDeleteError']
