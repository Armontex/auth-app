from typing import Protocol, TYPE_CHECKING
from common.ports import IUoW

if TYPE_CHECKING:
    from services.auth.app.ports import IUser


class IRole(Protocol):
    id: int
    name: str
    users: list["IUser"]
    permissions: list["IPermission"]


class IPermission(Protocol):
    id: int
    code: str
    roles: list["IRole"]


class IRoleRepository(Protocol):

    async def get_by_name(self, name: str) -> IRole | None: ...
    async def upsert(self, name: str) -> int: ...


class IPermissionRepository(Protocol):

    async def get_by_code(self, code: str) -> IPermission | None: ...
    async def upsert(self, code: str) -> int: ...


class IUserRolesRepository(Protocol):

    async def ensure_link(self, user_id: int, role_id: int) -> None: ...


class IRolePermissionsRepository(Protocol):

    async def ensure_link(self, role_id: int, permission_id: int) -> None: ...
    async def delete_link(self, role_id: int, permission_id: int) -> None: ...
    async def get_permissions_for_role(self, role_id: int) -> set[int]: ...
