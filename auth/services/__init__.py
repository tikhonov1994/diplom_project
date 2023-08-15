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

RoleServiceDep = Annotated[RoleService, Depends()]
UserServiceDep = Annotated[UserService, Depends()]
AuthServiceDep = Annotated[AuthService, Depends()]

__all__ = ['RoleServiceDep',
           'UserServiceDep',
           'AuthServiceDep',
           'ServiceItemNotFound',
           'ServiceConflictOnAddError',
           'ServiceConflictOnDeleteError',
           'ServiceUniqueFieldViolation',
           'ServiceItemSearchException']
