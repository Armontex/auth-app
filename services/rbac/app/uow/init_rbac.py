from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession

from common.base.uow import BaseUoW

from services.rbac.infra.db.permissions.repos import PermissionRepository
from services.rbac.infra.db.roles.repos import RoleRepository
from services.rbac.infra.db.role_permissions.repos import RolePermissionsRepository

from ..ports import (
    IPermissionRepository,
    IRoleRepository,
    IRolePermissionsRepository,
)


@dataclass
class Repos:
    role: IRoleRepository
    perm: IPermissionRepository
    role_perms: IRolePermissionsRepository


class InitRbacUoW(BaseUoW[Repos]):

    async def _init(self, session: AsyncSession) -> Repos:
        return Repos(
            role=RoleRepository(session),
            perm=PermissionRepository(session),
            role_perms=RolePermissionsRepository(session),
        )
