from services.auth.app.exc import UserNotExists

from ..ports import IRoleRepository, IUserRolesRepository
from ..exc import RoleNotFound
from ..uow import SetRoleUoW

from ...domain.const import Role


class SetRoleUseCase:

    def __init__(self, uow: SetRoleUoW) -> None:
        self._uow = uow

    @staticmethod
    async def set_role(
        user_id: int,
        role: Role,
        role_repo: IRoleRepository,
        user_roles_repo: IUserRolesRepository,
    ) -> None:
        """
        Raises:
            RoleNotFound: Роль не найдена.
        """
        role_obj = await role_repo.get_by_name(role.value)
        if not role_obj:
            raise RoleNotFound(role.value)

        await user_roles_repo.ensure_link(user_id, role_obj.id)

    async def execute(
        self,
        user_id: int,
        role: Role,
    ) -> None:
        """
        Raises:
            RoleNotFound: Роль не найдена.
            UserNotExists: Такого пользователя не существует.
        """
        async with self._uow as repos:
            if not repos.user.get_active_user_by_id(user_id):
                raise UserNotExists
            await self.set_role(user_id, role, repos.role, repos.user_roles)
