import pytest
from unittest.mock import AsyncMock, MagicMock

from services.register.app.usecases.register import RegisterUseCase
from services.rbac.domain.const import Role


async def test_register_usecase_success():
    auth_form = MagicMock()
    profile_form = MagicMock()

    user_repo = MagicMock()
    profile_repo = MagicMock()
    role_repo = MagicMock()
    user_roles_repo = MagicMock()

    repos = MagicMock(
        user=user_repo,
        profile=profile_repo,
        role=role_repo,
        user_roles=user_roles_repo,
    )
    uow = MagicMock()
    uow.__aenter__ = AsyncMock(return_value=repos)
    uow.__aexit__ = AsyncMock(return_value=False)

    hasher = MagicMock()

    auth_register_uc = AsyncMock()
    user = MagicMock()
    user.id = 123
    auth_register_uc.execute = AsyncMock(return_value=user)

    def make_auth_register(repo, hasher):
        return auth_register_uc

    profile_register_uc = AsyncMock()
    profile_register_uc.execute = AsyncMock()

    def make_profile_register(repo):
        return profile_register_uc

    set_role = AsyncMock()

    uc = RegisterUseCase(
        uow=uow,
        password_hasher=hasher,
        make_auth_register=make_auth_register,
        make_profile_register=make_profile_register,
        set_role=set_role,
    )

    result = await uc.execute(auth_form, profile_form)

    uow.__aenter__.assert_awaited_once()
    auth_register_uc.execute.assert_awaited_once_with(auth_form)
    profile_register_uc.execute.assert_awaited_once_with(user.id, profile_form)
    set_role.assert_awaited_once_with(user.id, Role.USER, role_repo, user_roles_repo)
    assert result is user
