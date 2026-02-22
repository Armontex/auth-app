from ..uow import InitRbacUoW
from ...domain.const import Permission, Role, ROLE_PERMISSIONS


class InitRbacUseCase:

    def __init__(
        self,
        uow: InitRbacUoW,
    ) -> None:
        self._uow = uow

    async def execute(self) -> None:
        async with self._uow as repos:

            role_ids: dict[Role, int] = {}
            for role in Role:
                role_ids[role] = await repos.role.upsert(role.value)

            permission_ids: dict[Permission, int] = {}
            for perm in Permission:
                permission_ids[perm] = await repos.perm.upsert(perm.value)

            for role, perms in ROLE_PERMISSIONS.items():
                role_id = role_ids[role]

                current_perm_ids = await repos.role_perms.get_permissions_for_role(
                    role_id
                )

                desired_perm_ids = {permission_ids[p] for p in perms}

                for perm_id in desired_perm_ids - current_perm_ids:
                    await repos.role_perms.ensure_link(role_id, perm_id)

                for perm_id in current_perm_ids - desired_perm_ids:
                    await repos.role_perms.delete_link(role_id, perm_id)
