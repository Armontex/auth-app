from ..ports import IUoW, IRoleRepository, IUserRolesRepository
from ..exc import (
    RoleNotFound,
)
from ...domain.const import Role


class SetRoleUseCase:

    def __init__(self, uow: IUoW[tuple[IRoleRepository, IUserRolesRepository]]) -> None:
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
        """
        async with self._uow as (role_repo, user_roles_repo):
            await self.set_role(user_id, role, role_repo, user_roles_repo)
