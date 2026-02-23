from fastapi import Depends
from common.ports import IUser
from api.v1.deps import get_rbac_container, RequirePermission
from services.rbac.app.usecases import (
    ReadMeRolesUseCase,
    ReadRolesUseCase,
    SetRoleUseCase,
)
from services.rbac.domain.const import Permission
from services.rbac.app.containers import RbacContainer


def get_read_me_roles_usecase(
    container: RbacContainer = Depends(get_rbac_container),
) -> ReadMeRolesUseCase:
    return container.read_me_roles_usecase()


def get_read_roles_usecase(
    container: RbacContainer = Depends(get_rbac_container),
) -> ReadRolesUseCase:
    return container.read_roles_usecase()


def get_set_role_usecase(
    container: RbacContainer = Depends(get_rbac_container),
) -> SetRoleUseCase:
    return container.set_role_usecase()


async def require_role_me_read() -> IUser:
    return await RequirePermission(Permission.ROLE_ME_READ)()


async def require_role_read() -> IUser:
    return await RequirePermission(Permission.ROLE_READ)()


async def require_role_set() -> IUser:
    return await RequirePermission(Permission.ROLE_SET)()
