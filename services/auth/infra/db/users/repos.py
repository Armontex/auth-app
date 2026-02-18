from typing import override
from common.base.db import BaseRepository
from common.exc import RepositoryError
from services.auth.app.ports import IUsersRepository
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from .models import User


class UserRepository(BaseRepository, IUsersRepository):

    @override
    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email).limit(1)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    @override
    async def add_user(
        self,
        first_name: str,
        middle_name: str | None,
        last_name: str,
        email: str,
        password_hash: str,
    ) -> User:
        new_user = User(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            email=email,
            password_hash=password_hash,
        )
        try:
            async with self._session.begin():
                self._session.add(new_user)
                await self._session.flush()
        except IntegrityError as e:
            raise RepositoryError("email already exists") from e

        await self._session.refresh(new_user)
        return new_user
