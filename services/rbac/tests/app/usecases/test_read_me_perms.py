import pytest
from unittest.mock import AsyncMock, MagicMock

from services.rbac.app.usecases import ReadMePermissionsUseCase
from common.ports import IUser, IPermission


def make_user(user_id: int) -> IUser:
    user = MagicMock(spec=IUser)
    user.id = user_id
    return user


def make_permission(code: str) -> IPermission:
    perm = MagicMock(spec=IPermission)
    perm.code = code
    return perm


async def test_readme_permissions_delegates_to_read_perms():
    read_perms_uc = AsyncMock()
    user = make_user(123)

    uc = ReadMePermissionsUseCase(read_perms=read_perms_uc)

    perms = {make_permission("READ"), make_permission("WRITE")}
    read_perms_uc.execute.return_value = perms

    result = await uc.execute(user)

    read_perms_uc.execute.assert_awaited_once_with(123)
    assert result == perms


async def test_readme_permissions_returns_empty_set_from_read_perms():
    read_perms_uc = AsyncMock()
    user = make_user(1)

    uc = ReadMePermissionsUseCase(read_perms=read_perms_uc)

    read_perms_uc.execute.return_value = set()

    result = await uc.execute(user)

    read_perms_uc.execute.assert_awaited_once_with(1)
    assert result == set()
