import pytest
from unittest.mock import AsyncMock, MagicMock

from services.rbac.app.usecases import ReadPermissionsUseCase, ReadMePermissionsUseCase
from services.auth.app.exc import UserNotExists
from common.ports import IUser, IPermission



async def test_read_permissions_returns_permissions_for_existing_user():
    user_id = 1

    user: IUser = MagicMock(spec=IUser)
    perms: set[IPermission] = {MagicMock(spec=IPermission), MagicMock(spec=IPermission)}

    user_repo = MagicMock()
    user_repo.get_active_user_by_id = AsyncMock(return_value=user)

    uow = MagicMock()
    uow.__aenter__ = AsyncMock(return_value=MagicMock(user=user_repo))
    uow.__aexit__ = AsyncMock(return_value=False)

    read_me_perms = MagicMock(spec=ReadMePermissionsUseCase)
    read_me_perms.execute.return_value = perms

    uc = ReadPermissionsUseCase(uow=uow, read_me_perms=read_me_perms)

    result = await uc.execute(user_id)

    user_repo.get_active_user_by_id.assert_awaited_once_with(user_id)
    read_me_perms.execute.assert_called_once_with(user)
    assert result is perms



async def test_read_permissions_raises_when_user_not_found():
    user_id = 42

    user_repo = MagicMock()
    user_repo.get_active_user_by_id = AsyncMock(return_value=None)

    uow = MagicMock()
    uow.__aenter__ = AsyncMock(return_value=MagicMock(user=user_repo))
    uow.__aexit__ = AsyncMock(return_value=False)

    read_me_perms = MagicMock(spec=ReadMePermissionsUseCase)

    uc = ReadPermissionsUseCase(uow=uow, read_me_perms=read_me_perms)

    with pytest.raises(UserNotExists):
        await uc.execute(user_id)

    user_repo.get_active_user_by_id.assert_awaited_once_with(user_id)
    read_me_perms.execute.assert_not_called()
