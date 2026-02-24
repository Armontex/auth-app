import pytest
from unittest.mock import AsyncMock, MagicMock

from services.rbac.app.usecases import ReadRolesUseCase
from services.auth.app.exc import UserNotExists
from common.ports import IUser, IRole


@pytest.mark.asyncio
async def test_read_roles_returns_roles_for_existing_user():
    user_id = 1

    r1 = MagicMock(spec=IRole)
    r2 = MagicMock(spec=IRole)
    user: IUser = MagicMock(spec=IUser)
    user.roles = [r1, r2]

    user_repo = MagicMock()
    user_repo.get_active_user_by_id = AsyncMock(return_value=user)

    uow = MagicMock()
    uow.__aenter__ = AsyncMock(return_value=MagicMock(user=user_repo))
    uow.__aexit__ = AsyncMock(return_value=False)

    uc = ReadRolesUseCase(uow=uow)

    result = await uc.execute(user_id)

    user_repo.get_active_user_by_id.assert_awaited_once_with(user_id)
    assert result == [r1, r2]


@pytest.mark.asyncio
async def test_read_roles_raises_when_user_not_found():
    user_id = 42

    user_repo = MagicMock()
    user_repo.get_active_user_by_id = AsyncMock(return_value=None)

    uow = MagicMock()
    uow.__aenter__ = AsyncMock(return_value=MagicMock(user=user_repo))
    uow.__aexit__ = AsyncMock(return_value=False)

    uc = ReadRolesUseCase(uow=uow)

    with pytest.raises(UserNotExists):
        await uc.execute(user_id)

    user_repo.get_active_user_by_id.assert_awaited_once_with(user_id)
