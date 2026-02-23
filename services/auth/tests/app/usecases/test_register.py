import pytest
from unittest.mock import AsyncMock, Mock, MagicMock

from services.auth.app.usecases.register import RegisterUseCase


@pytest.fixture
def repo_mock():
    repo = AsyncMock()
    repo.add = AsyncMock()
    return repo


@pytest.fixture
def hasher_mock():
    hasher = Mock()
    hasher.hash = Mock()
    return hasher


@pytest.fixture
def usecase(repo_mock, hasher_mock):
    return RegisterUseCase(repo=repo_mock, password_hasher=hasher_mock)


async def test_execute_hashes_password_and_calls_repo_add(
    usecase, repo_mock, hasher_mock
):
    form = MagicMock()
    form.email.value = "user@example.com"
    form.password.value = "plain-password"

    hasher_mock.hash.return_value = "hashed-password"
    created_user = MagicMock()
    repo_mock.add.return_value = created_user

    result = await usecase.execute(form)

    hasher_mock.hash.assert_called_once_with("plain-password")
    repo_mock.add.assert_awaited_once_with(
        email="user@example.com",
        password_hash="hashed-password",
    )
    assert result is created_user
