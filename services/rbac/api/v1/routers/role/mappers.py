from services.rbac.app.exc import RoleNotFound
from services.rbac.domain.const import Role
from common.ports import IRole
from .schemas import ReadRolesResponse


def map_role_name_to_role(role_name: str) -> Role:
    """
    Raises:
        RoleNotFound: Роль не найдена
    """
    try:
        return Role(role_name)
    except ValueError as e:
        raise RoleNotFound(role_name) from e


def map_roles_to_response(roles: list[IRole]) -> ReadRolesResponse:
    return ReadRolesResponse(roles=[r.name for r in roles])
