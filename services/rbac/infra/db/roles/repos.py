from services.rbac.app.ports import IRoleRepository
from sqlalchemy import select, insert
from typing import override

from common.base.db import BaseRepository
from .models import Role


class RoleRepository(BaseRepository, IRoleRepository):

    @override
    async def get_by_name(self, name: str) -> Role | None:
        stmt = select(Role).where(Role.name == name)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    @override
    async def upsert(self, name: str) -> int:
        stmt = select(Role).where(Role.name == name)
        res = await self._session.execute(stmt)
        if obj := res.scalar_one_or_none():
            return obj.id

        stmt = insert(Role).values(name=name).returning(Role.id)
        res = await self._session.execute(stmt)
        return res.scalar_one()
