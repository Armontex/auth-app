import pytest
from unittest.mock import AsyncMock, MagicMock

from fastapi import status

from services.rbac.app.usecases import ReadPermissionsUseCase
from services.rbac.api.v1.routers.permission.deps import (
    get_read_perms_usecase,
    require_permission_read,
)
from services.auth.app.exc import UserNotExists


@pytest.fixture
def read_perms_usecase_mock() -> AsyncMock:
    uc = AsyncMock(spec=ReadPermissionsUseCase)
    uc.execute = AsyncMock()
    return uc


@pytest.fixture(autouse=True)
def override_deps(app_for_tests, read_perms_usecase_mock):
    def fake_require_permission_read():
        user = MagicMock()
        return user

    app_for_tests.dependency_overrides[require_permission_read] = (
        fake_require_permission_read
    )
    app_for_tests.dependency_overrides[get_read_perms_usecase] = (
        lambda: read_perms_usecase_mock
    )
    yield
    app_for_tests.dependency_overrides.clear()


def _url(user_id: int) -> str:
    return f"/api/v1/rbac/permission/?user_id={user_id}"


def test_read_permissions_success(client, read_perms_usecase_mock):
    read_perms_usecase_mock.execute.return_value = {"permissions": ["P1", "P2"]}

    response = client.get(_url(10))

    assert response.status_code == status.HTTP_200_OK
    read_perms_usecase_mock.execute.assert_awaited_once_with(10)
    assert response.json() == {"permissions": ["P1", "P2"]}


def test_read_permissions_user_not_exists(client, read_perms_usecase_mock):
    err = UserNotExists("User not exists.")

    async def failing_execute(user_id: int):
        raise err

    read_perms_usecase_mock.execute.side_effect = failing_execute

    response = client.get(_url(999))

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "User not exists."}
