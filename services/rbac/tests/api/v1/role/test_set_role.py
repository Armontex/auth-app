import pytest
from unittest.mock import AsyncMock, MagicMock

from fastapi import status

from services.rbac.app.usecases import SetRoleUseCase
from services.rbac.app.exc import RoleNotFound
from services.auth.app.exc import UserNotExists
from services.rbac.api.v1.routers.role.deps import (
    get_set_role_usecase,
    require_role_set,
)
from services.rbac.api.v1.routers.role import mappers
from services.rbac.domain.const import Role


@pytest.fixture
def set_role_usecase_mock() -> AsyncMock:
    uc = AsyncMock(spec=SetRoleUseCase)
    uc.execute = AsyncMock()
    return uc


@pytest.fixture(autouse=True)
def override_deps(app_for_tests, set_role_usecase_mock):
    def fake_require_role_set():
        return MagicMock()

    app_for_tests.dependency_overrides[require_role_set] = fake_require_role_set
    app_for_tests.dependency_overrides[get_set_role_usecase] = (
        lambda: set_role_usecase_mock
    )
    yield
    app_for_tests.dependency_overrides.clear()


def _url() -> str:
    return "/api/v1/rbac/role/"


def test_set_role_success(client, set_role_usecase_mock, monkeypatch):
    monkeypatch.setattr(mappers, "map_role_name_to_role", lambda name: Role.ADMIN)

    body = {"user_id": 10, "role": "admin"}

    response = client.post(_url(), json=body)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    set_role_usecase_mock.execute.assert_awaited_once_with(10, Role.ADMIN)


def test_set_role_role_not_found(client, set_role_usecase_mock, monkeypatch):
    monkeypatch.setattr(mappers, "map_role_name_to_role", lambda name: Role.ADMIN)

    err = RoleNotFound("Role 'unknown' not found.")

    async def failing_execute(user_id: int, role):
        raise err

    set_role_usecase_mock.execute.side_effect = failing_execute

    body = {"user_id": 10, "role": "unknown"}

    response = client.post(_url(), json=body)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Role 'unknown' not found."}


def test_set_role_user_not_exists(client, set_role_usecase_mock, monkeypatch):
    monkeypatch.setattr(mappers, "map_role_name_to_role", lambda name: Role.ADMIN)

    err = UserNotExists("User not exists.")

    async def failing_execute(user_id: int, role):
        raise err

    set_role_usecase_mock.execute.side_effect = failing_execute

    body = {"user_id": 999, "role": "admin"}

    response = client.post(_url(), json=body)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "User not exists."}
