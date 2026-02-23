import pytest
from unittest.mock import AsyncMock, MagicMock

from fastapi import status

from services.rbac.app.usecases import ReadMePermissionsUseCase
from services.rbac.api.v1.routers.permission.deps import (
    get_read_me_perms_usecase,
    require_permission_me_read,
)


@pytest.fixture
def read_me_perms_usecase_mock() -> AsyncMock:
    uc = AsyncMock(spec=ReadMePermissionsUseCase)
    uc.execute = MagicMock()
    return uc


@pytest.fixture(autouse=True)
def override_deps(app_for_tests, read_me_perms_usecase_mock):
    def fake_require_permission_me_read():
        user = MagicMock()
        return user

    app_for_tests.dependency_overrides[require_permission_me_read] = (
        fake_require_permission_me_read
    )
    app_for_tests.dependency_overrides[get_read_me_perms_usecase] = (
        lambda: read_me_perms_usecase_mock
    )
    yield
    app_for_tests.dependency_overrides.clear()


def _url() -> str:
    return "/api/v1/rbac/permission/me"


def test_read_me_permissions_success(client, read_me_perms_usecase_mock):
    read_me_perms_usecase_mock.execute.return_value = {"permissions": ["P1", "P2"]}

    response = client.get(_url())

    assert response.status_code == status.HTTP_200_OK
    read_me_perms_usecase_mock.execute.assert_called_once()
    assert response.json() == {"permissions": ["P1", "P2"]}
