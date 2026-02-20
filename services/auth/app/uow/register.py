from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from services.auth.app.ports import IRegisterUoW, IUserRepository, IProfileRepository
from services.auth.infra.db.users.repos import UserRepository
from services.profile.infra.db.profiles.repos import ProfileRepository


class RegisterUoW(IRegisterUoW):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def __aenter__(self) -> tuple[IUserRepository, IProfileRepository]:
        self._session = self._session_factory()
        self._user_repo = UserRepository(self._session)
        self._profile_repo = ProfileRepository(self._session)
        return self._user_repo, self._profile_repo

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type:
            await self._session.rollback()
        else:
            await self._session.commit()
        await self._session.close()
