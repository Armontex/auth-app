import pytest
from unittest.mock import AsyncMock

from fastapi import status

from services.auth.api.v1.deps import get_login_usecase
from services.auth.app.usecases import LoginUseCase, LoginError


@pytest.fixture
def override_login_usecase(app_for_tests):
    mock = AsyncMock(spec=LoginUseCase)

    async def _override():
        return mock

    app_for_tests.dependency_overrides[get_login_usecase] = _override
    yield mock
    app_for_tests.dependency_overrides.clear()


def test_login_success(client, override_login_usecase):
    override_login_usecase.execute.return_value = "jwt-token-123"

    resp = client.post(
        "/api/v1/auth/login",
        json={"email": "ivan@example.com", "password": "secret123"},
        headers={"Content-Type": "application/json"},
    )

    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == {"access_token": "jwt-token-123"}
    override_login_usecase.execute.assert_awaited_once()


def test_login_validation_error(client, override_login_usecase):
    resp = client.post(
        "/api/v1/auth/login",
        json={"email": "not-email", "password": "secret123"},
        headers={"Content-Type": "application/json"},
    )

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json() == {"detail": {"email": ["Invalid email address"]}}


def test_login_invalid_credentials(client, override_login_usecase):
    override_login_usecase.execute.side_effect = LoginError("Invalid credentials.")

    resp = client.post(
        "/api/v1/auth/login",
        json={"email": "ivan@example.com", "password": "wrong-password"},
        headers={"Content-Type": "application/json"},
    )

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED
    assert resp.json() == {"detail": "Invalid credentials."}


def test_login_unsupported_content_type(client, override_login_usecase):
    resp = client.post(
        "/api/v1/auth/login",
        json={"email": "ivan@example.com", "password": "secret123"},
        headers={"Content-Type": "text/plain"},
    )

    assert resp.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    assert resp.json() == {
        "detail": "Content-Type must be application/json",
    }
