import pytest
from unittest.mock import AsyncMock

from services.auth.app.usecases.logout import LogoutUseCase


@pytest.fixture
def jwt_mock():
    jwt = AsyncMock()
    jwt.revoke = AsyncMock()
    return jwt


@pytest.fixture
def usecase(jwt_mock):
    return LogoutUseCase(jwt_manager=jwt_mock)


async def test_execute_calls_jwt_revoke(usecase, jwt_mock):
    token = "access-token"

    await usecase.execute(token)

    jwt_mock.revoke.assert_awaited_once_with(token)
