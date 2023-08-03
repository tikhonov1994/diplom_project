from typing import Annotated

from fastapi import Depends

from services.role import RoleService
from services.user import UserService
from services.exceptions import (ServiceItemNotFound,
                                 ServiceConflictOnAddError,
                                 ServiceConflictOnDeleteError)

RoleServiceDep = Annotated[RoleService, Depends()]
UserServiceDep = Annotated[UserService, Depends()]

__all__ = ['RoleServiceDep',
           'UserServiceDep',
           'ServiceItemNotFound',
           'ServiceConflictOnAddError',
           'ServiceConflictOnDeleteError']
