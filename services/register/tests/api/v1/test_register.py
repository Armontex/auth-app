import pytest
from unittest.mock import AsyncMock, MagicMock

from fastapi import status

from services.register.api.v1.routers.register.deps import (
    get_register_usecase,
    validate_content_type,
)
from services.register.app.usecases import RegisterUseCase
from services.auth.domain.exc import ValidationError as AuthValidationError
from services.profile.domain.exc import ValidationError as ProfileValidationError
from services.auth.app.exc import EmailAlreadyExists
from services.profile.app.exc import ProfileAlreadyExists


@pytest.fixture
def register_usecase_mock() -> AsyncMock:
    uc = AsyncMock(spec=RegisterUseCase)
    uc.execute = AsyncMock()
    return uc


@pytest.fixture(autouse=True)
def override_deps(app_for_tests, register_usecase_mock):
    def fake_validate_content_type():
        return None

    app_for_tests.dependency_overrides[validate_content_type] = (
        fake_validate_content_type
    )
    app_for_tests.dependency_overrides[get_register_usecase] = (
        lambda: register_usecase_mock
    )
    yield
    app_for_tests.dependency_overrides.clear()


def _url() -> str:
    return "/api/v1/register/"


def _body(**overrides) -> dict:
    base = {
        "email": "user@example.com",
        "first_name": "John",
        "middle_name": "M",
        "last_name": "Doe",
        "password": "strongpwd",
        "confirm_password": "strongpwd",
    }
    base.update(overrides)
    return base


def test_register_success(client, register_usecase_mock):
    user = MagicMock()
    user.id = 123
    user.email = "user@example.com"
    register_usecase_mock.execute.return_value = user

    resp = client.post(_url(), json=_body())

    assert resp.status_code == status.HTTP_201_CREATED
    register_usecase_mock.execute.assert_awaited_once()
    assert resp.json() == {"id": 123, "email": "user@example.com"}


def test_register_auth_validation_error(client, register_usecase_mock):
    err = AuthValidationError(errors={"password": ["too short (min 8)"]})

    async def failing_execute(auth_form, profile_form):
        raise err

    register_usecase_mock.execute.side_effect = failing_execute

    resp = client.post(
        _url(),
        json=_body(password="short", confirm_password="short"),
    )

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json() == {"detail": {"password": ["too short (min 8)"]}}


def test_register_profile_validation_error(client, register_usecase_mock):
    err = ProfileValidationError(errors={"value": ["cannot be empty"]})

    async def failing_execute(auth_form, profile_form):
        raise err

    register_usecase_mock.execute.side_effect = failing_execute

    resp = client.post(_url(), json=_body(first_name=""))

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json() == {"detail": {"value": ["cannot be empty"]}}


def test_register_email_already_exists(client, register_usecase_mock):
    err = EmailAlreadyExists("Email already exists.")

    async def failing_execute(auth_form, profile_form):
        raise err

    register_usecase_mock.execute.side_effect = failing_execute

    resp = client.post(_url(), json=_body())

    assert resp.status_code == status.HTTP_409_CONFLICT
    assert resp.json() == {"detail": "Email already exists."}


def test_register_profile_already_exists(client, register_usecase_mock):
    err = ProfileAlreadyExists("Profile already exists.")

    async def failing_execute(auth_form, profile_form):
        raise err

    register_usecase_mock.execute.side_effect = failing_execute

    resp = client.post(_url(), json=_body())

    assert resp.status_code == status.HTTP_409_CONFLICT
    assert resp.json() == {"detail": "Profile already exists."}
