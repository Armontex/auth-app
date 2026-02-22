from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth.app.ports import IUserRepository
from services.auth.infra.db.users.repos import UserRepository

from services.profile.app.ports import IProfileRepository
from services.profile.infra.db.profiles.repos import ProfileRepository

from services.rbac.app.ports import IUserRolesRepository, IRoleRepository
from services.rbac.infra.db.roles.repos import RoleRepository
from services.rbac.infra.db.user_roles.repos import UserRolesRepository


@dataclass
class Repos:
    user: IUserRepository
    profile: IProfileRepository
    role: IRoleRepository
    user_roles: IUserRolesRepository

from common.base.uow import BaseUoW


class RegisterUoW(BaseUoW[Repos]):

    async def _init(self, session: AsyncSession) -> Repos:
        return Repos(
            user=UserRepository(session),
            profile=ProfileRepository(session),
            role=RoleRepository(session),
            user_roles=UserRolesRepository(session)
        )