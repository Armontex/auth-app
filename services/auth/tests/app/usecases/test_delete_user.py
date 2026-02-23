import pytest
from unittest.mock import AsyncMock, MagicMock

from services.auth.app.usecases.delete_user import DeleteUserUseCase


@pytest.fixture
def uow_mock():
    uow = AsyncMock()
    repos = MagicMock()
    repos.user = AsyncMock()
    repos.user.delete_user = AsyncMock()
    uow.__aenter__.return_value = repos
    return uow


@pytest.fixture
def logout_usecase_mock():
    uc = AsyncMock()
    uc.execute = AsyncMock()
    return uc


@pytest.fixture
def authorize_usecase_mock():
    uc = AsyncMock()
    uc.verify_token = AsyncMock()
    return uc


@pytest.fixture
def usecase(uow_mock, logout_usecase_mock, authorize_usecase_mock):
    return DeleteUserUseCase(
        uow=uow_mock,
        logout_usecase=logout_usecase_mock,
        authorize_usecase=authorize_usecase_mock,
    )


async def test_execute_verifies_deletes_and_logs_out(
    usecase, uow_mock, logout_usecase_mock, authorize_usecase_mock
):
    token = "access-token"
    authorize_usecase_mock.verify_token.return_value = 123

    await usecase.execute(token)

    authorize_usecase_mock.verify_token.assert_awaited_once_with(token)
    uow_mock.__aenter__.assert_awaited_once()
    uow_mock.__aenter__.return_value.user.delete_user.assert_awaited_once_with(123)
    logout_usecase_mock.execute.assert_awaited_once_with(token)
