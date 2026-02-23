import pytest
from unittest.mock import AsyncMock, MagicMock

from fastapi import status

from services.profile.app.usecases import ReadProfileUseCase
from services.profile.app.exc import ProfileNotFound
from services.profile.api.v1.routers.read.deps import (
    get_read_prof_usecase,
    require_profile_read,
)


@pytest.fixture
def read_prof_usecase_mock() -> AsyncMock:
    uc = AsyncMock(spec=ReadProfileUseCase)
    uc.execute = AsyncMock()
    return uc


@pytest.fixture(autouse=True)
def override_deps(app_for_tests, read_prof_usecase_mock):
    def fake_require_profile_read():
        user = MagicMock()
        return user

    app_for_tests.dependency_overrides[require_profile_read] = fake_require_profile_read
    app_for_tests.dependency_overrides[get_read_prof_usecase] = (
        lambda: read_prof_usecase_mock
    )
    yield
    app_for_tests.dependency_overrides.clear()


def _url(user_id: int) -> str:
    return f"/api/v1/profile/?user_id={user_id}"


def test_read_profile_success(client, read_prof_usecase_mock):
    profile = MagicMock()
    profile.first_name = "John"
    profile.last_name = "Doe"
    profile.middle_name = "Middle"
    read_prof_usecase_mock.execute.return_value = profile

    response = client.get(_url(10))

    assert response.status_code == status.HTTP_200_OK
    read_prof_usecase_mock.execute.assert_awaited_once_with(10)

    body = response.json()
    assert body["first_name"] == "John"
    assert body["last_name"] == "Doe"
    assert body["middle_name"] == "Middle"


def test_read_profile_not_found(client, read_prof_usecase_mock):
    err = ProfileNotFound("Profile not exists.")

    async def failing_execute(user_id: int):
        raise err

    read_prof_usecase_mock.execute.side_effect = failing_execute

    response = client.get(_url(999))

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Profile not exists."}
