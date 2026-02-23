import pytest
from unittest.mock import AsyncMock

from fastapi import status

from services.auth.app.usecases import LogoutUseCase
from services.auth.app.exc import TokenVerifyError
from services.auth.api.v1.routers.logout.deps import (
    get_logout_usecase,
    get_bearer_token,
)


@pytest.fixture
def usecase_mock() -> AsyncMock:
    uc = AsyncMock(spec=LogoutUseCase)
    uc.execute = AsyncMock()
    return uc


@pytest.fixture(autouse=True)
def override_deps(app_for_tests, usecase_mock):
    app_for_tests.dependency_overrides[get_logout_usecase] = lambda: usecase_mock
    app_for_tests.dependency_overrides[get_bearer_token] = lambda: "test-token"
    yield
    app_for_tests.dependency_overrides.clear()


def test_logout_success(client, usecase_mock):
    response = client.post("/api/v1/auth/logout")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    usecase_mock.execute.assert_awaited_once_with("test-token")


def test_logout_token_verify_error(client, usecase_mock):
    err = TokenVerifyError("invalid token")

    async def failing_execute(_):
        raise err

    usecase_mock.execute.side_effect = failing_execute

    response = client.post("/api/v1/auth/logout")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "invalid token"}
