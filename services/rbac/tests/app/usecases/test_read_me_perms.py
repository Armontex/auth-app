import pytest
from unittest.mock import MagicMock

from services.rbac.app.usecases import ReadMePermissionsUseCase
from common.ports import IUser, IPermission


def make_permission(code: str) -> IPermission:
    perm = MagicMock(spec=IPermission)
    perm.code = code
    return perm


def make_role(perms: list[IPermission]):
    role = MagicMock()
    role.permissions = perms
    return role


def make_user(roles):
    user = MagicMock(spec=IUser)
    user.roles = roles
    return user


def test_readme_permissions_returns_union_of_all_role_permissions():
    p_read = make_permission("READ")
    p_write = make_permission("WRITE")
    p_delete = make_permission("DELETE")

    role_1 = make_role([p_read, p_write])
    role_2 = make_role([p_write, p_delete])

    user = make_user([role_1, role_2])

    uc = ReadMePermissionsUseCase()

    result = uc.execute(user)

    assert result == {p_read, p_write, p_delete}


def test_readme_permissions_handles_user_without_roles():
    user = make_user([])

    uc = ReadMePermissionsUseCase()

    result = uc.execute(user)

    assert result == set()


def test_readme_permissions_handles_roles_without_permissions():
    role_1 = make_role([])
    role_2 = make_role([])

    user = make_user([role_1, role_2])

    uc = ReadMePermissionsUseCase()

    result = uc.execute(user)

    assert result == set()
