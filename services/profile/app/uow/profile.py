from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession

from common.base import BaseUoW

from services.profile.infra.db.profiles.repos import ProfileRepository

from ..ports import IProfileRepository


@dataclass
class Repos:
    profile: IProfileRepository


class ProfileUoW(BaseUoW[Repos]):

    async def _init(self, session: AsyncSession) -> Repos:
        return Repos(profile=ProfileRepository(session))
