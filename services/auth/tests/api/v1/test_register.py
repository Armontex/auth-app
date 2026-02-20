import pytest
from unittest.mock import AsyncMock

from fastapi import status

from services.auth.api.v1.deps import get_register_usecase
from services.auth.app.usecases import RegisterUseCase, RegisterError


@pytest.fixture
def override_register_usecase(app_for_tests):
    mock = AsyncMock(spec=RegisterUseCase)

    async def _override():
        return mock

    app_for_tests.dependency_overrides[get_register_usecase] = _override
    yield mock
    app_for_tests.dependency_overrides.clear()


def test_register_success(client, override_register_usecase):
    class FakeUser:
        def __init__(self, id: int, email: str) -> None:
            self.id = id
            self.email = email

    override_register_usecase.execute.return_value = FakeUser(
        id=1, email="ivan@example.com"
    )

    resp = client.post(
        "/api/v1/auth/register",
        json={
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "email": "ivan@example.com",
            "password": "secret123",
            "confirm_password": "secret123",
        },
        headers={"Content-Type": "application/json"},
    )

    assert resp.status_code == status.HTTP_201_CREATED
    assert resp.json() == {"id": 1, "email": "ivan@example.com"}
    override_register_usecase.execute.assert_awaited_once()


def test_register_validation_error(client, override_register_usecase):
    resp = client.post(
        "/api/v1/auth/register",
        json={
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "email": "not-email",
            "password": "secret123",
            "confirm_password": "different",
        },
        headers={"Content-Type": "application/json"},
    )

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json() == {"detail": {"email": ["invalid email address"]}}


def test_register_conflict_email(client, override_register_usecase):
    override_register_usecase.execute.side_effect = RegisterError(
        "User with this email already exists."
    )

    resp = client.post(
        "/api/v1/auth/register",
        json={
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "email": "ivan@example.com",
            "password": "secret123",
            "confirm_password": "secret123",
        },
        headers={"Content-Type": "application/json"},
    )

    assert resp.status_code == status.HTTP_409_CONFLICT
    assert resp.json() == {"detail": "User with this email already exists."}


def test_register_unsupported_content_type(client, override_register_usecase):
    resp = client.post(
        "/api/v1/auth/register",
        json={
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "email": "ivan@example.com",
            "password": "secret123",
            "confirm_password": "secret123",
        },
        headers={"Content-Type": "text/plain"},
    )

    assert resp.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    assert resp.json() == {
        "detail": "Content-Type must be application/json",
    }
