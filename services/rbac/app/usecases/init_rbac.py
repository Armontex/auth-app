from ..ports import (
    IRoleRepository,
    IPermissionRepository,
    IRolePermissionsRepository,
    IUoW,
)

from ...domain.const import Permission, Role, ROLE_PERMISSIONS


class InitRbacUseCase:

    def __init__(
        self,
        uow: IUoW[
            tuple[IRoleRepository, IPermissionRepository, IRolePermissionsRepository]
        ],
    ) -> None:
        self._uow = uow

    async def execute(self) -> None:
        async with self._uow as (role_repo, permission_repo, role_permissions_repo):
            role_ids: dict[Role, int] = {}
            for role in Role:
                role_ids[role] = await role_repo.upsert(role.value)

            permission_ids: dict[Permission, int] = {}
            for perm in Permission:
                permission_ids[perm] = await permission_repo.upsert(perm.value)

            for role, perms in ROLE_PERMISSIONS.items():
                role_id = role_ids[role]

                current_perm_ids = await role_permissions_repo.get_permissions_for_role(
                    role_id
                )

                desired_perm_ids = {permission_ids[p] for p in perms}

                for perm_id in desired_perm_ids - current_perm_ids:
                    await role_permissions_repo.ensure_link(role_id, perm_id)

                for perm_id in current_perm_ids - desired_perm_ids:
                    await role_permissions_repo.delete_link(role_id, perm_id)
