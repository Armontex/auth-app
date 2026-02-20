import pytest

from services.auth.app.usecases.delete_user import (
    DeleteUserUseCase,
    DeleteUserError,
)
from services.auth.common.exc import InfraError
from common.exc import RepositoryError


@pytest.fixture
def use_case(user_uow, jwt_manager):
    return DeleteUserUseCase(uow=user_uow, jwt_manager=jwt_manager)


@pytest.mark.asyncio
async def test_delete_user_success(use_case, user_uow, user_repo, jwt_manager):
    token = "valid.jwt.token"
    user_id = 42

    jwt_manager.verify.return_value = user_id

    await use_case.execute(token)

    jwt_manager.verify.assert_awaited_once_with(token)
    jwt_manager.revoke.assert_awaited_once_with(token)
    user_repo.delete_user.assert_awaited_once_with(user_id)
    user_uow.__aenter__.assert_awaited_once()
    user_uow.__aexit__.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_user_raises_on_infra_error(
    use_case, jwt_manager, user_repo, user_uow
):
    token = "bad.jwt.token"
    jwt_manager.verify.side_effect = InfraError("redis down")

    with pytest.raises(DeleteUserError) as exc_info:
        await use_case.execute(token)

    assert "Invalid or expired token" in str(exc_info.value)
    jwt_manager.verify.assert_awaited_once_with(token)
    jwt_manager.revoke.assert_not_awaited()
    user_repo.delete_user.assert_not_awaited()
    user_uow.__aenter__.assert_not_awaited()
    user_uow.__aexit__.assert_not_awaited()


@pytest.mark.asyncio
async def test_delete_user_raises_on_repository_error(
    use_case, jwt_manager, user_repo, user_uow
):
    token = "valid.jwt.token"
    user_id = 42

    jwt_manager.verify.return_value = user_id
    user_repo.delete_user.side_effect = RepositoryError("db error")

    with pytest.raises(DeleteUserError) as exc_info:
        await use_case.execute(token)

    assert "This user does not exist" in str(exc_info.value)
    jwt_manager.verify.assert_awaited_once_with(token)
    jwt_manager.revoke.assert_awaited_once_with(token)
    user_repo.delete_user.assert_awaited_once_with(user_id)
    user_uow.__aenter__.assert_awaited_once()
    user_uow.__aexit__.assert_awaited_once()
