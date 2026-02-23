from services.rbac.app.exc import RoleNotFound
from services.rbac.domain.const import Role


def map_role_name_to_role(role_name: str) -> Role:
    """
    Raises:
        RoleNotFound: Роль не найдена
    """
    try:
        return Role(role_name)
    except ValueError as e:
        raise RoleNotFound(role_name) from e
