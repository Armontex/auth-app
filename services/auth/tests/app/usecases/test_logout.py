import pytest
from services.auth.app.usecases.logout import LogoutUseCase, LogoutError
from services.auth.common.exc import InfraError


@pytest.fixture
def use_case(jwt_manager):
    return LogoutUseCase(jwt_manager=jwt_manager)



async def test_logout_calls_revoke_on_jwt_manager(use_case, jwt_manager):
    token = "some.jwt.token"

    await use_case.execute(token)

    jwt_manager.revoke.assert_awaited_once_with(token)



async def test_logout_raises_logout_error_on_infra_error(use_case, jwt_manager):
    token = "bad.jwt.token"
    jwt_manager.revoke.side_effect = InfraError("redis down")

    with pytest.raises(LogoutError) as exc_info:
        await use_case.execute(token)

    assert "Invalid or expired token" in str(exc_info.value)
    jwt_manager.revoke.assert_awaited_once_with(token)
