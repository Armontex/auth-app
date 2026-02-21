from typing import override
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from common.base.db import BaseRepository

from services.profile.app.ports import IProfile, IProfileRepository
from services.profile.app.exc import ProfileAlreadyExists
from .models import Profile


class ProfileRepository(BaseRepository, IProfileRepository):

    @override
    async def add(
        self,
        user_id: int,
        first_name: str,
        middle_name: str | None,
        last_name: str,
    ) -> Profile:
        new_profile = Profile(
            user_id=user_id,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
        )
        try:
            self._session.add(new_profile)
            await self._session.flush()
        except IntegrityError as e:
            raise ProfileAlreadyExists() from e

        await self._session.refresh(new_profile)
        return new_profile

    @override
    async def get_by_user_id(self, user_id: int) -> Profile | None:
        stmt = select(Profile).where(Profile.user_id == user_id).limit(1)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    @override
    async def set_first_name(self, profile: IProfile, new_first_name: str) -> None:
        profile.first_name = new_first_name

    @override
    async def set_last_name(self, profile: IProfile, new_last_name: str) -> None:
        profile.last_name = new_last_name

    @override
    async def set_middle_name(
        self, profile: IProfile, new_middle_name: str | None
    ) -> None:
        profile.middle_name = new_middle_name
