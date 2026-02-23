import pytest
from unittest.mock import AsyncMock

from fastapi import status

from services.auth.app.usecases import ChangeEmailUseCase
from services.auth.app.exc import LoginError, EmailAlreadyExists
from services.auth.domain.exc import ValidationError
from services.auth.api.v1.routers.change_email.deps import get_change_email_usecase


@pytest.fixture
def usecase_mock() -> AsyncMock:
    return AsyncMock(spec=ChangeEmailUseCase)


@pytest.fixture(autouse=True)
def override_usecase(app_for_tests, usecase_mock):
    app_for_tests.dependency_overrides[get_change_email_usecase] = lambda: usecase_mock
    yield
    app_for_tests.dependency_overrides.clear()


def _valid_body():
    return {
        "email": "user@example.com",
        "password": "old-password",
        "new_email": "new@example.com",
    }


def test_change_email_success(client, usecase_mock):
    response = client.post("/api/v1/auth/change-email", json=_valid_body())

    assert response.status_code == status.HTTP_204_NO_CONTENT
    usecase_mock.execute.assert_awaited_once()


def test_change_email_validation_error(client, usecase_mock):
    err = ValidationError(errors={"field": ["msg"]})

    async def failing_execute(_):
        raise err

    usecase_mock.execute.side_effect = failing_execute

    response = client.post("/api/v1/auth/change-email", json=_valid_body())

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": {"field": ["msg"]}}


def test_change_email_login_error(client, usecase_mock):
    err = LoginError("invalid credentials")

    async def failing_execute(_):
        raise err

    usecase_mock.execute.side_effect = failing_execute

    response = client.post("/api/v1/auth/change-email", json=_valid_body())

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "invalid credentials"}


def test_change_email_email_already_exists(client, usecase_mock):
    err = EmailAlreadyExists("email already exists")

    async def failing_execute(_):
        raise err

    usecase_mock.execute.side_effect = failing_execute

    response = client.post("/api/v1/auth/change-email", json=_valid_body())

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {"detail": "email already exists"}
