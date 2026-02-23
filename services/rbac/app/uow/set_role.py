from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession

from common.base import BaseUoW

from services.auth.app.ports import IUserRepository
from services.auth.infra.db.users.repos import UserRepository

from services.rbac.infra.db.roles.repos import RoleRepository
from services.rbac.infra.db.user_roles.repos import UserRolesRepository

from ..ports import (
    IRoleRepository,
    IUserRolesRepository,
)


@dataclass
class Repos:
    role: IRoleRepository
    user: IUserRepository
    user_roles: IUserRolesRepository


class SetRoleUoW(BaseUoW[Repos]):

    async def _init(self, session: AsyncSession) -> Repos:
        return Repos(
            user=UserRepository(session),
            role=RoleRepository(session),
            user_roles=UserRolesRepository(session),
        )
