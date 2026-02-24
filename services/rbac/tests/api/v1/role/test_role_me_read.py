import pytest
from unittest.mock import AsyncMock, MagicMock

from fastapi import status

from services.rbac.app.usecases import ReadMeRolesUseCase
from services.rbac.api.v1.routers.role.deps import (
    get_read_me_roles_usecase,
    require_role_me_read,
)
from common.ports import IRole


@pytest.fixture
def read_me_roles_usecase_mock() -> AsyncMock:
    uc = AsyncMock(spec=ReadMeRolesUseCase)
    uc.execute = AsyncMock()
    return uc


@pytest.fixture(autouse=True)
def override_deps(app_for_tests, read_me_roles_usecase_mock):
    def fake_require_role_me_read():
        user = MagicMock()
        return user

    app_for_tests.dependency_overrides[require_role_me_read] = fake_require_role_me_read
    app_for_tests.dependency_overrides[get_read_me_roles_usecase] = (
        lambda: read_me_roles_usecase_mock
    )
    yield
    app_for_tests.dependency_overrides.clear()


def _url() -> str:
    return "/api/v1/rbac/role/me"


def test_read_me_roles_success(client, read_me_roles_usecase_mock):
    r1 = MagicMock(spec=IRole)
    r1.name = "admin"
    r2 = MagicMock(spec=IRole)
    r2.name = "user"

    read_me_roles_usecase_mock.execute.return_value = [r1, r2]

    response = client.get(_url())

    assert response.status_code == status.HTTP_200_OK
    read_me_roles_usecase_mock.execute.assert_awaited_once()

    assert response.json() == {"roles": ["admin", "user"]}
