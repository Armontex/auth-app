from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from ..ports import (
    IUoW,
    IRoleRepository,
    IUserRolesRepository,
)

from services.rbac.infra.db.roles.repos import RoleRepository
from services.rbac.infra.db.user_roles.repos import UserRolesRepository


class SetRoleUoW(IUoW[tuple[IRoleRepository, IUserRolesRepository]]):

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]) -> None:
        self._session_maker = session_maker

    async def __aenter__(
        self,
    ) -> tuple[IRoleRepository, IUserRolesRepository]:
        self._session = self._session_maker()
        role_repo = RoleRepository(self._session)
        user_roles_repo = UserRolesRepository(self._session)
        return (
            role_repo,
            user_roles_repo,
        )

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type:
            await self._session.rollback()
        else:
            await self._session.commit()
        await self._session.close()
