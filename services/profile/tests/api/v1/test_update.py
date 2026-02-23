import pytest
from unittest.mock import AsyncMock, MagicMock

from fastapi import status

from services.profile.app.usecases import UpdateUseCase
from services.profile.domain.exc import ValidationError
from services.profile.api.v1.routers.update.deps import (
    get_update_usecase,
    require_profile_me_update,
)


@pytest.fixture
def update_usecase_mock() -> AsyncMock:
    uc = AsyncMock(spec=UpdateUseCase)
    uc.execute = AsyncMock()
    return uc


@pytest.fixture(autouse=True)
def override_deps(app_for_tests, update_usecase_mock):
    def fake_require_profile_me_update():
        user = MagicMock()
        user.profile = MagicMock()
        return user

    app_for_tests.dependency_overrides[require_profile_me_update] = (
        fake_require_profile_me_update
    )
    app_for_tests.dependency_overrides[get_update_usecase] = (
        lambda: update_usecase_mock
    )
    yield
    app_for_tests.dependency_overrides.clear()


def _body():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "middle_name": "Middle",
    }


def test_update_profile_success(client, update_usecase_mock):
    profile = MagicMock()
    profile.first_name = "John"
    profile.last_name = "Doe"
    profile.middle_name = "Middle"
    update_usecase_mock.execute.return_value = profile

    response = client.put("/api/v1/profile/me", json=_body())

    assert response.status_code == status.HTTP_200_OK
    update_usecase_mock.execute.assert_awaited_once()
    data = response.json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["middle_name"] == "Middle"


def test_update_profile_validation_error(client, update_usecase_mock):
    err = ValidationError(errors={"field": ["msg"]})

    async def failing_execute(user, form):
        raise err

    update_usecase_mock.execute.side_effect = failing_execute

    response = client.put("/api/v1/profile/me", json=_body())

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": {"field": ["msg"]}}