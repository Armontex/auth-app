import pytest
from unittest.mock import AsyncMock, MagicMock

from services.rbac.app.usecases import ReadRolesUseCase, ReadMeRolesUseCase
from services.auth.app.exc import UserNotExists
from common.ports import IUser, IRole


async def test_read_roles_returns_roles_for_existing_user():
    user_id = 1

    user: IUser = MagicMock(spec=IUser)
    roles: list[IRole] = [MagicMock(spec=IRole), MagicMock(spec=IRole)]

    user_repo = MagicMock()
    user_repo.get_active_user_by_id = AsyncMock(return_value=user)

    uow = MagicMock()
    uow.__aenter__ = AsyncMock(return_value=MagicMock(user=user_repo))
    uow.__aexit__ = AsyncMock(return_value=False)

    read_me_roles = MagicMock(spec=ReadMeRolesUseCase)
    read_me_roles.execute.return_value = roles

    uc = ReadRolesUseCase(uow=uow, read_me_roles=read_me_roles)

    result = await uc.execute(user_id)

    user_repo.get_active_user_by_id.assert_awaited_once_with(user_id)
    read_me_roles.execute.assert_called_once_with(user)
    assert result is roles


async def test_read_roles_raises_when_user_not_found():
    user_id = 42

    user_repo = MagicMock()
    user_repo.get_active_user_by_id = AsyncMock(return_value=None)

    uow = MagicMock()
    uow.__aenter__ = AsyncMock(return_value=MagicMock(user=user_repo))
    uow.__aexit__ = AsyncMock(return_value=False)

    read_me_roles = MagicMock(spec=ReadMeRolesUseCase)

    uc = ReadRolesUseCase(uow=uow, read_me_roles=read_me_roles)

    with pytest.raises(UserNotExists):
        await uc.execute(user_id)

    user_repo.get_active_user_by_id.assert_awaited_once_with(user_id)
    read_me_roles.execute.assert_not_called()
