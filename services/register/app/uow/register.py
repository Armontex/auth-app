from ..ports import IUoW
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from services.auth.app.ports import IUserRepository
from services.auth.infra.db.users.repos import UserRepository

from services.profile.app.ports import IProfileRepository
from services.profile.infra.db.profiles.repos import ProfileRepository

from services.rbac.app.ports import IUserRolesRepository, IRoleRepository
from services.rbac.infra.db.roles.repos import RoleRepository
from services.rbac.infra.db.user_roles.repos import UserRolesRepository

Repositories = tuple[
    IUserRepository, IProfileRepository, IRoleRepository, IUserRolesRepository
]


class RegisterUoW(IUoW[Repositories]):

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]) -> None:
        self._session_maker = session_maker

    async def __aenter__(self) -> Repositories:
        self._session = self._session_maker()
        auth_repo = UserRepository(self._session)
        profile_repo = ProfileRepository(self._session)
        role_repo = RoleRepository(self._session)
        user_roles_repo = UserRolesRepository(self._session)
        return auth_repo, profile_repo, role_repo, user_roles_repo

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type:
            await self._session.rollback()
        else:
            await self._session.commit()
        await self._session.close()
