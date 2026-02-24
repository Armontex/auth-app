import pytest
from unittest.mock import AsyncMock, MagicMock

from services.rbac.app.usecases import ReadMeRolesUseCase
from common.ports import IUser, IRole


def make_user(user_id: int) -> IUser:
    user = MagicMock(spec=IUser)
    user.id = user_id
    return user


def make_role(name: str) -> IRole:
    role = MagicMock(spec=IRole)
    role.name = name
    return role


@pytest.mark.asyncio
async def test_readme_roles_delegates_to_read_roles():
    read_roles_uc = AsyncMock()
    user = make_user(123)

    uc = ReadMeRolesUseCase(read_roles=read_roles_uc)

    r1 = make_role("admin")
    r2 = make_role("manager")
    read_roles_uc.execute.return_value = [r1, r2]

    result = await uc.execute(user)

    read_roles_uc.execute.assert_awaited_once_with(123)
    assert result == [r1, r2]


@pytest.mark.asyncio
async def test_readme_roles_returns_empty_list_from_read_roles():
    read_roles_uc = AsyncMock()
    user = make_user(1)

    uc = ReadMeRolesUseCase(read_roles=read_roles_uc)

    read_roles_uc.execute.return_value = []

    result = await uc.execute(user)

    read_roles_uc.execute.assert_awaited_once_with(1)
    assert result == []
