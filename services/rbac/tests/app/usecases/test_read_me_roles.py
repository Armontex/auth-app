import pytest
from unittest.mock import MagicMock

from services.rbac.app.usecases import ReadMeRolesUseCase
from common.ports import IUser, IRole


def make_role(name: str) -> IRole:
    role = MagicMock(spec=IRole)
    role.name = name
    return role


def make_user(roles: list[IRole]) -> IUser:
    user = MagicMock(spec=IUser)
    user.roles = roles
    return user


def test_readme_roles_returns_user_roles():
    r1 = make_role("admin")
    r2 = make_role("manager")
    user = make_user([r1, r2])

    uc = ReadMeRolesUseCase()

    result = uc.execute(user)

    assert result == [r1, r2]


def test_readme_roles_handles_user_without_roles():
    user = make_user([])

    uc = ReadMeRolesUseCase()

    result = uc.execute(user)

    assert result == []
