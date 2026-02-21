from ..ports import IUoW
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from services.auth.app.ports import IUserRepository
from services.auth.infra.db.users.repos import UserRepository

from services.profile.app.ports import IProfileRepository
from services.profile.infra.db.profiles.repos import ProfileRepository


class RegisterUoW(IUoW[tuple[IUserRepository, IProfileRepository]]):

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]) -> None:
        self._session_maker = session_maker

    async def __aenter__(self) -> tuple[IUserRepository, IProfileRepository]:
        self._session = self._session_maker()
        auth_repo = UserRepository(self._session)
        profile_repo = ProfileRepository(self._session)
        return auth_repo, profile_repo

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type:
            await self._session.rollback()
        else:
            await self._session.commit()
        await self._session.close()
