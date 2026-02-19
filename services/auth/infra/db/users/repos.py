from typing import override
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from common.base.db import BaseRepository
from common.exc import RepositoryError
from services.auth.app.ports import IUserRepository
from .models import User


class UserRepository(BaseRepository, IUserRepository):

    # @override
    # async def get_user_by_email(
    #     self, email: str, is_active: bool = True
    # ) -> User | None:
    #     """Данная функция выдаёт первого user-а (активного по-умолчанию) с равным `email` или,
    #     если пользователь с такой почтой не существует, то `None`

    #     Args:
    #         email (str): Почта
    #         is_active (bool, optional): Активный ли пользователь. По-умолчанию: True.

    #     Returns:
    #         User | None: `User` - если такой пользователь найден, иначе `None`
    #     """
    #     stmt = (
    #         select(User)
    #         .where((User.email == email) and (User.is_active == is_active))
    #         .limit(1)
    #     )
    #     result = await self._session.execute(stmt)
    #     return result.scalars().first()

    @override
    async def add_user(
        self,
        first_name: str,
        middle_name: str | None,
        last_name: str,
        email: str,
        password_hash: str,
    ) -> User:
        """Данная функция создаёт нового user-а

        Args:
            first_name (str): Имя
            middle_name (str | None): Отчество (или None, если нет)
            last_name (str): Фамилия
            email (str): Почта
            password_hash (str): Хеш пароля

        Raises:
            RepositoryError: Если пользователь с таким `email` уже существует

        Returns:
            User: Добавленный user
        """
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
