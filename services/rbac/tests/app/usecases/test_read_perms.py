import pytest
from unittest.mock import AsyncMock, MagicMock

from services.rbac.app.usecases import ReadPermissionsUseCase
from services.auth.app.exc import UserNotExists
from common.ports import IUser, IPermission


@pytest.mark.asyncio
async def test_read_permissions_returns_permissions_for_existing_user():
    user_id = 1

    p1 = MagicMock(spec=IPermission)
    p2 = MagicMock(spec=IPermission)
    role_1 = MagicMock()
    role_1.permissions = [p1]
    role_2 = MagicMock()
    role_2.permissions = [p1, p2]

    user: IUser = MagicMock(spec=IUser)
    user.roles = [role_1, role_2]

    user_repo = MagicMock()
    user_repo.get_active_user_by_id = AsyncMock(return_value=user)

    uow = MagicMock()
    uow.__aenter__ = AsyncMock(return_value=MagicMock(user=user_repo))
    uow.__aexit__ = AsyncMock(return_value=False)

    uc = ReadPermissionsUseCase(uow=uow)

    result = await uc.execute(user_id)

    user_repo.get_active_user_by_id.assert_awaited_once_with(user_id)
    assert result == {p1, p2}


@pytest.mark.asyncio
async def test_read_permissions_raises_when_user_not_found():
    user_id = 42

    user_repo = MagicMock()
    user_repo.get_active_user_by_id = AsyncMock(return_value=None)

    uow = MagicMock()
    uow.__aenter__ = AsyncMock(return_value=MagicMock(user=user_repo))
    uow.__aexit__ = AsyncMock(return_value=False)

    uc = ReadPermissionsUseCase(uow=uow)

    with pytest.raises(UserNotExists):
        await uc.execute(user_id)

    user_repo.get_active_user_by_id.assert_awaited_once_with(user_id)
