import pytest
from unittest.mock import MagicMock
from fastapi import status

from services.profile.app.usecases import ReadMeProfileUseCase
from services.profile.api.v1.routers.read.deps import (
    get_read_me_prof_usecase,
    require_profile_me_read,
)


@pytest.fixture
def read_me_usecase_mock() -> MagicMock:
    uc = MagicMock(spec=ReadMeProfileUseCase)
    uc.execute = MagicMock()
    return uc


@pytest.fixture(autouse=True)
def override_deps(app_for_tests, read_me_usecase_mock):
    def fake_user_dep():
        user = MagicMock()
        user.id = 123
        return user

    app_for_tests.dependency_overrides[require_profile_me_read] = fake_user_dep
    app_for_tests.dependency_overrides[get_read_me_prof_usecase] = (
        lambda: read_me_usecase_mock
    )
    yield
    app_for_tests.dependency_overrides.clear()


def test_read_me_profile_success(client, read_me_usecase_mock):
    profile = MagicMock()
    profile.first_name = "John"
    profile.last_name = "Doe"
    profile.middle_name = "Middle"

    async def _exec(user):
        return profile

    read_me_usecase_mock.execute.side_effect = _exec

    response = client.get("/api/v1/profile/me")

    assert response.status_code == status.HTTP_200_OK
    read_me_usecase_mock.execute.assert_called_once()

    body = response.json()
    assert body["first_name"] == "John"
    assert body["last_name"] == "Doe"
    assert body["middle_name"] == "Middle"
