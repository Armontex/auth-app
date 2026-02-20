from typing import override
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from common.base.db import BaseRepository
from common.exc import RepositoryError
from services.auth.app.ports import IUserRepository
from .models import User


class UserRepository(BaseRepository, IUserRepository):

    @override
    async def get_user_by_email(
        self, email: str, is_active: bool = True
    ) -> User | None:
        stmt = (
            select(User)
            .where((User.email == email) & (User.is_active == is_active))
            .limit(1)
        )
        result = await self._session.execute(stmt)
        return result.scalars().first()

    @override
    async def add(
        self,
        email: str,
        password_hash: str,
    ) -> User:
        new_user = User(
            email=email,
            password_hash=password_hash,
        )
        try:
            self._session.add(new_user)
            await self._session.flush()
        except IntegrityError as e:
            raise RepositoryError("Email already exists") from e

        await self._session.refresh(new_user)
        return new_user

    @override
    async def delete_user(self, user_id: int) -> None:
        user = await self._session.get(User, user_id)
        if not user or not user.is_active:
            raise RepositoryError("User does not exist")

        user.is_active = False
