from typing import override
from sqlalchemy import select, insert, delete
from services.rbac.app.ports import IRolePermissionsRepository
from common.base.db import BaseRepository
from .models import role_permissions


class RolePermissionsRepository(BaseRepository, IRolePermissionsRepository):

    @override
    async def ensure_link(self, role_id: int, permission_id: int) -> None:
        stmt = select(role_permissions).where(
            role_permissions.c.role_id == role_id,
            role_permissions.c.permission_id == permission_id,
        )
        res = await self._session.execute(stmt)
        if res.scalar_one_or_none():
            return

        stmt = insert(role_permissions).values(
            role_id=role_id,
            permission_id=permission_id,
        )
        await self._session.execute(stmt)

    @override
    async def delete_link(self, role_id: int, permission_id: int) -> None:
        stmt = delete(role_permissions).where(
            role_permissions.c.role_id == role_id,
            role_permissions.c.permission_id == permission_id,
        )
        await self._session.execute(stmt)

    @override
    async def get_permissions_for_role(self, role_id: int) -> set[int]:
        stmt = select(role_permissions.c.permission_id).where(
            role_permissions.c.role_id == role_id
        )
        res = await self._session.execute(stmt)
        return {row[0] for row in res.all()}
