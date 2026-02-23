import pytest
from unittest.mock import AsyncMock

from fastapi import status

from services.auth.app.usecases import DeleteUserUseCase
from services.auth.app.exc import UserNotExists, TokenVerifyError
from services.auth.api.v1.routers.delete_user.deps import (
    get_delete_user_usecase,
    get_bearer_token,
)


@pytest.fixture
def usecase_mock() -> AsyncMock:
    uc = AsyncMock(spec=DeleteUserUseCase)
    uc.execute = AsyncMock()
    return uc


@pytest.fixture(autouse=True)
def override_deps(app_for_tests, usecase_mock):
    app_for_tests.dependency_overrides[get_delete_user_usecase] = lambda: usecase_mock
    app_for_tests.dependency_overrides[get_bearer_token] = lambda: "test-token"
    yield
    app_for_tests.dependency_overrides.clear()


def test_delete_user_success(client, usecase_mock):
    response = client.delete("/api/v1/auth/")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    usecase_mock.execute.assert_awaited_once_with("test-token")


def test_delete_user_user_not_exists(client, usecase_mock):
    err = UserNotExists("user not exists")

    async def failing_execute(_):
        raise err

    usecase_mock.execute.side_effect = failing_execute

    response = client.delete("/api/v1/auth/")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "user not exists"}


def test_delete_user_token_verify_error(client, usecase_mock):
    err = TokenVerifyError("invalid token")

    async def failing_execute(_):
        raise err

    usecase_mock.execute.side_effect = failing_execute

    response = client.delete("/api/v1/auth/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "invalid token"}
