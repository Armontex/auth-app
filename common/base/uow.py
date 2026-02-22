from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from ..ports import IUoW


class BaseUoW[T](IUoW[T], ABC):

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]) -> None:
        self._session_maker = session_maker

    @abstractmethod
    async def _init(self, session: AsyncSession) -> T:
        pass

    async def __aenter__(
        self,
    ) -> T:
        self._session = self._session_maker()
        return await self._init(self._session)

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type:
            await self._session.rollback()
        else:
            await self._session.commit()
        await self._session.close()
