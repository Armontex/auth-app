from typing import override
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from common.base.db import BaseRepository
from services.auth.app.ports import IUserRepository
from services.auth.app.exc import EmailAlreadyExists, UserNotExists
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
    async def get_active_user_by_id(self, id: int) -> User | None:
        user = await self._session.get(User, id)
        return None if (not user or not user.is_active) else user

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

        self._session.add(new_user)

        try:
            await self._session.flush()
        except IntegrityError as e:
            raise EmailAlreadyExists() from e

        await self._session.refresh(new_user)
        return new_user

    @override
    async def delete_user(self, user_id: int) -> None:
        user = await self.get_active_user_by_id(user_id)
        if not user:
            raise UserNotExists()

        user.is_active = False

    @override
    async def set_email(self, user: User, new_email: str) -> None:
        user = await self._session.merge(user)
        user.email = new_email
        try:
            await self._session.flush()
        except IntegrityError as e:
            raise EmailAlreadyExists() from e

    @override
    async def set_password_hash(self, user: User, new_password_hash: str) -> None:
        user = await self._session.merge(user)
        user.password_hash = new_password_hash
