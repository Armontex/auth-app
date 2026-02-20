from typing import override
from sqlalchemy.exc import IntegrityError

from common.base.db import BaseRepository
from common.exc import RepositoryError

from services.profile.app.ports import IProfileRepository
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
            raise RepositoryError("A profile for the user already exists") from e

        await self._session.refresh(new_profile)
        return new_profile
