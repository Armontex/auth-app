import pytest
from unittest.mock import AsyncMock, MagicMock

from fastapi import status

from services.rbac.app.usecases import ReadRolesUseCase
from services.rbac.api.v1.routers.role.deps import (
    get_read_roles_usecase,
    require_role_read,
)
from services.auth.app.exc import UserNotExists
from common.ports import IRole


@pytest.fixture
def read_roles_usecase_mock() -> AsyncMock:
    uc = AsyncMock(spec=ReadRolesUseCase)
    uc.execute = AsyncMock()
    return uc


@pytest.fixture(autouse=True)
def override_deps(app_for_tests, read_roles_usecase_mock):
    def fake_require_role_read():
        user = MagicMock()
        return user

    app_for_tests.dependency_overrides[require_role_read] = fake_require_role_read
    app_for_tests.dependency_overrides[get_read_roles_usecase] = (
        lambda: read_roles_usecase_mock
    )
    yield
    app_for_tests.dependency_overrides.clear()


def _url(user_id: int) -> str:
    return f"/api/v1/rbac/role/?user_id={user_id}"


def test_read_roles_success(client, read_roles_usecase_mock):
    r1 = MagicMock(spec=IRole)
    r1.name = "admin"
    r2 = MagicMock(spec=IRole)
    r2.name = "user"

    read_roles_usecase_mock.execute.return_value = [r1, r2]

    response = client.get(_url(10))

    assert response.status_code == status.HTTP_200_OK
    read_roles_usecase_mock.execute.assert_awaited_once_with(10)
    assert response.json() == {"roles": ["admin", "user"]}


def test_read_roles_user_not_exists(client, read_roles_usecase_mock):
    read_roles_usecase_mock.execute.side_effect = UserNotExists("User not exists.")

    response = client.get(_url(999))

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "User not exists."}
