from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from services.profile.app.ports import IProfileUoW, IProfileRepository
from services.profile.infra.db.profiles.repos import ProfileRepository


class ProfileUoW(IProfileUoW):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def __aenter__(self) -> IProfileRepository:
        self._session = self._session_factory()
        self._repo = ProfileRepository(self._session)
        return self._repo

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type:
            await self._session.rollback()
        else:
            await self._session.commit()
        await self._session.close()
