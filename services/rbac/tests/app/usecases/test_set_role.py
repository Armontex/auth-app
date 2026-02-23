import pytest
from unittest.mock import AsyncMock, MagicMock

from services.rbac.app.usecases.set_role import SetRoleUseCase
from services.rbac.domain.const import Role
from services.rbac.app.exc import RoleNotFound
from services.auth.app.exc import UserNotExists


async def test_set_role_static_sets_link_when_role_exists():
    user_id = 1
    role = Role.ADMIN

    role_obj = MagicMock()
    role_obj.id = 10

    role_repo = MagicMock()
    role_repo.get_by_name = AsyncMock(return_value=role_obj)

    user_roles_repo = MagicMock()
    user_roles_repo.ensure_link = AsyncMock()

    await SetRoleUseCase.set_role(user_id, role, role_repo, user_roles_repo)

    role_repo.get_by_name.assert_awaited_once_with(role.value)
    user_roles_repo.ensure_link.assert_awaited_once_with(user_id, role_obj.id)


async def test_set_role_static_raises_when_role_not_found():
    user_id = 1
    role = Role.ADMIN

    role_repo = MagicMock()
    role_repo.get_by_name = AsyncMock(return_value=None)

    user_roles_repo = MagicMock()
    user_roles_repo.ensure_link = AsyncMock()

    with pytest.raises(RoleNotFound):
        await SetRoleUseCase.set_role(user_id, role, role_repo, user_roles_repo)

    role_repo.get_by_name.assert_awaited_once_with(role.value)
    user_roles_repo.ensure_link.assert_not_awaited()


async def test_execute_raises_when_user_not_found():
    user_id = 1
    role = Role.ADMIN

    user_repo = MagicMock()
    user_repo.get_active_user_by_id = AsyncMock(return_value=None)

    role_repo = MagicMock()
    role_repo.get_by_name = AsyncMock()
    user_roles_repo = MagicMock()
    user_roles_repo.ensure_link = AsyncMock()

    uow = MagicMock()
    uow.__aenter__ = AsyncMock(
        return_value=MagicMock(
            user=user_repo,
            role=role_repo,
            user_roles=user_roles_repo,
        )
    )
    uow.__aexit__ = AsyncMock(return_value=False)

    uc = SetRoleUseCase(uow)

    with pytest.raises(UserNotExists):
        await uc.execute(user_id, role)

    user_repo.get_active_user_by_id.assert_awaited_once_with(user_id)
    role_repo.get_by_name.assert_not_awaited()
    user_roles_repo.ensure_link.assert_not_awaited()


async def test_execute_calls_set_role_when_user_exists(monkeypatch):
    user_id = 1
    role = Role.ADMIN

    user_repo = MagicMock()
    user_repo.get_active_user_by_id = AsyncMock(return_value=MagicMock())

    role_repo = MagicMock()
    user_roles_repo = MagicMock()

    uow = MagicMock()
    uow.__aenter__ = AsyncMock(
        return_value=MagicMock(
            user=user_repo,
            role=role_repo,
            user_roles=user_roles_repo,
        )
    )
    uow.__aexit__ = AsyncMock(return_value=False)

    uc = SetRoleUseCase(uow)

    called = {}

    async def fake_set_role(self, uid, r, rr, urr):
        called["args"] = (uid, r, rr, urr)

    monkeypatch.setattr(SetRoleUseCase, "set_role", fake_set_role)

    await uc.execute(user_id, role)

    user_repo.get_active_user_by_id.assert_awaited_once_with(user_id)
    assert called["args"] == (user_id, role, role_repo, user_roles_repo)
