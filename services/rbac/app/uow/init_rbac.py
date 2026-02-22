from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from ..ports import (
    IUoW,
    IPermissionRepository,
    IRoleRepository,
    IRolePermissionsRepository,
)

from services.rbac.infra.db.permissions.repos import PermissionRepository
from services.rbac.infra.db.roles.repos import RoleRepository
from services.rbac.infra.db.role_permissions.repos import RolePermissionsRepository


class InitRbacUoW(
    IUoW[tuple[IRoleRepository, IPermissionRepository, IRolePermissionsRepository]]
):

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]) -> None:
        self._session_maker = session_maker

    async def __aenter__(
        self,
    ) -> tuple[IRoleRepository, IPermissionRepository, IRolePermissionsRepository]:
        self._session = self._session_maker()
        permission_repo = PermissionRepository(self._session)
        role_repo = RoleRepository(self._session)
        role_permissions_repo = RolePermissionsRepository(self._session)
        return (
            role_repo,
            permission_repo,
            role_permissions_repo,
        )

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type:
            await self._session.rollback()
        else:
            await self._session.commit()
        await self._session.close()
