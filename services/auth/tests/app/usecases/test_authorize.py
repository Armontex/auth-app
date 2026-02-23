import pytest
from unittest.mock import AsyncMock, MagicMock

from services.auth.app.usecases.authorize import AuthorizeUseCase
from services.auth.app.exc import UserNotExists


@pytest.fixture
def jwt_mock():
    jwt = AsyncMock()
    jwt.verify = AsyncMock(return_value=42)
    return jwt


@pytest.fixture
def uow_mock():
    uow = AsyncMock()
    repos = MagicMock()
    repos.user = AsyncMock()
    repos.user.get_active_user_by_id = AsyncMock()
    uow.__aenter__.return_value = repos
    return uow


@pytest.fixture
def usecase(uow_mock, jwt_mock):
    return AuthorizeUseCase(uow=uow_mock, jwt_manager=jwt_mock)



async def test_verify_token_delegates_to_jwt_manager(usecase, jwt_mock):
    token = "access-token"

    user_id = await usecase.verify_token(token)

    jwt_mock.verify.assert_awaited_once_with(token)
    assert user_id == jwt_mock.verify.return_value



async def test_execute_returns_user_when_found(usecase, uow_mock, jwt_mock):
    token = "access-token"
    jwt_mock.verify.return_value = 10

    fake_user = MagicMock()
    uow_mock.__aenter__.return_value.user.get_active_user_by_id.return_value = fake_user

    result = await usecase.execute(token)

    jwt_mock.verify.assert_awaited_once_with(token)
    uow_mock.__aenter__.return_value.user.get_active_user_by_id.assert_awaited_once_with(
        10
    )
    assert result is fake_user



async def test_execute_raises_user_not_exists_when_user_missing(
    usecase, uow_mock, jwt_mock
):
    token = "access-token"
    jwt_mock.verify.return_value = 99

    uow_mock.__aenter__.return_value.user.get_active_user_by_id.return_value = None

    with pytest.raises(UserNotExists):
        await usecase.execute(token)

    jwt_mock.verify.assert_awaited_once_with(token)
    uow_mock.__aenter__.return_value.user.get_active_user_by_id.assert_awaited_once_with(
        99
    )
