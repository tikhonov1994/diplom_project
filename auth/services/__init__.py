from typing import Annotated

from fastapi import Depends

from services.role import RoleService

RoleServiceDep = Annotated[RoleService, Depends()]

__all__ = ['RoleServiceDep']
