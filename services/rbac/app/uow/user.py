from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession

from common.base import BaseUoW

from services.auth.app.ports import IUserRepository
from services.auth.infra.db.users.repos import UserRepository


@dataclass
class Repos:
    user: IUserRepository


class UserUoW(BaseUoW[Repos]):

    async def _init(self, session: AsyncSession) -> Repos:
        return Repos(user=UserRepository(session))
