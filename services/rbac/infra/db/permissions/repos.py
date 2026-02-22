from services.rbac.app.ports import IPermissionRepository
from sqlalchemy import select, insert
from typing import override

from common.base.db import BaseRepository
from .models import Permission


class PermissionRepository(BaseRepository, IPermissionRepository):

    @override
    async def get_by_code(self, code: str) -> Permission | None:
        stmt = select(Permission).where(Permission.code == code)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    @override
    async def upsert(self, code: str) -> int:
        stmt = select(Permission).where(Permission.code == code)
        res = await self._session.execute(stmt)
        if obj := res.scalar_one_or_none():
            return obj.id

        stmt = insert(Permission).values(code=code).returning(Permission.id)
        res = await self._session.execute(stmt)
        return res.scalar_one()
