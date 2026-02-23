import pytest
from unittest.mock import AsyncMock
from fastapi import status

from services.auth.app.usecases import ChangePasswordUseCase
from services.auth.app.exc import LoginError
from services.auth.domain.exc import ValidationError
from services.auth.api.v1.routers.change_password.deps import (
    get_change_password_usecase,
)


@pytest.fixture
def usecase_mock() -> AsyncMock:
    uc = AsyncMock(spec=ChangePasswordUseCase)
    uc.execute = AsyncMock()
    return uc


@pytest.fixture(autouse=True)
def override_usecase(app_for_tests, usecase_mock):
    app_for_tests.dependency_overrides[get_change_password_usecase] = (
        lambda: usecase_mock
    )
    yield
    app_for_tests.dependency_overrides.clear()


def _valid_body():
    return {
        "email": "user@example.com",
        "old_password": "old-password",
        "new_password": "new-password",
    }


def test_change_password_success(client, usecase_mock):
    response = client.post("/api/v1/auth/change-password", json=_valid_body())

    assert response.status_code == status.HTTP_204_NO_CONTENT
    usecase_mock.execute.assert_awaited_once()


def test_change_password_validation_error(client, usecase_mock):
    err = ValidationError(errors={"field": ["msg"]})

    async def failing_execute(_):
        raise err

    usecase_mock.execute.side_effect = failing_execute

    response = client.post("/api/v1/auth/change-password", json=_valid_body())

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": {"field": ["msg"]}}


def test_change_password_login_error(client, usecase_mock):
    err = LoginError("invalid credentials")

    async def failing_execute(_):
        raise err

    usecase_mock.execute.side_effect = failing_execute

    response = client.post("/api/v1/auth/change-password", json=_valid_body())

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "invalid credentials"}
