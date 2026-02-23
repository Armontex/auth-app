import pytest
from unittest.mock import AsyncMock, MagicMock, Mock

from services.auth.app.usecases.change_password import ChangePasswordUseCase


@pytest.fixture
def uow_mock():
    uow = AsyncMock()
    repos = MagicMock()
    repos.user = AsyncMock()
    repos.user.set_password_hash = AsyncMock()
    uow.__aenter__.return_value = repos
    return uow


@pytest.fixture
def hasher_mock():
    hasher = Mock()
    hasher.hash = Mock()
    return hasher


@pytest.fixture
def login_usecase_mock():
    usecase = AsyncMock()
    usecase.authenticate = AsyncMock()
    return usecase


@pytest.fixture
def usecase(uow_mock, hasher_mock, login_usecase_mock):
    return ChangePasswordUseCase(
        uow=uow_mock,
        password_hasher=hasher_mock,
        login_usecase=login_usecase_mock,
    )


async def test_execute_authenticates_hashes_and_sets_password(
    usecase, uow_mock, hasher_mock, login_usecase_mock
):
    form = MagicMock()
    form.new_password.value = "new-password"

    user = MagicMock()
    login_usecase_mock.authenticate.return_value = user
    hasher_mock.hash.return_value = "hashed-new-password"

    await usecase.execute(form)

    login_usecase_mock.authenticate.assert_awaited_once_with(form)
    hasher_mock.hash.assert_called_once_with("new-password")
    uow_mock.__aenter__.assert_awaited_once()
    uow_mock.__aenter__.return_value.user.set_password_hash.assert_awaited_once_with(
        user, "hashed-new-password"
    )
