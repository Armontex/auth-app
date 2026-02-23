import pytest
from unittest.mock import AsyncMock, MagicMock

from services.auth.app.usecases.change_email import ChangeEmailUseCase


@pytest.fixture
def uow_mock():
    uow = AsyncMock()
    repos = MagicMock()
    repos.user = AsyncMock()
    repos.user.set_email = AsyncMock()
    uow.__aenter__.return_value = repos
    return uow


@pytest.fixture
def login_usecase_mock():
    usecase = AsyncMock()
    usecase.authenticate = AsyncMock()
    return usecase


@pytest.fixture
def usecase(uow_mock, login_usecase_mock):
    return ChangeEmailUseCase(uow=uow_mock, login_usecase=login_usecase_mock)



async def test_execute_authenticates_and_sets_email(
    usecase, uow_mock, login_usecase_mock
):
    form = MagicMock()
    form.new_email.value = "new@example.com"

    user = MagicMock()
    login_usecase_mock.authenticate.return_value = user

    await usecase.execute(form)

    login_usecase_mock.authenticate.assert_awaited_once_with(form)
    uow_mock.__aenter__.assert_awaited_once()
    uow_mock.__aenter__.return_value.user.set_email.assert_awaited_once_with(
        user, "new@example.com"
    )
