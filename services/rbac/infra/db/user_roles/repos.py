from services.rbac.app.ports import IUserRolesRepository
from sqlalchemy import select, insert
from typing import override

from common.base.db import BaseRepository
from .models import user_roles


class UserRolesRepository(BaseRepository, IUserRolesRepository):

    @override
    async def ensure_link(self, user_id: int, role_id: int) -> None:
        stmt = select(user_roles).where(
            user_roles.c.user_id == user_id,
            user_roles.c.role_id == role_id,
        )
        res = await self._session.execute(stmt)
        if res.scalar_one_or_none():
            return

        stmt = insert(user_roles).values(
            user_id=user_id,
            role_id=role_id,
        )
        await self._session.execute(stmt)
