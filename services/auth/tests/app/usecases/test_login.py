import pytest
from unittest.mock import Mock

from services.auth.app.usecases.login import LoginUseCase, LoginError
from services.auth.domain.models.login import LoginForm
from services.auth.domain.models.email import EmailAddress


@pytest.fixture
def use_case(user_uow, password_hasher, jwt_manager):
    return LoginUseCase(
        uow=user_uow,
        password_hasher=password_hasher,
        jwt_manager=jwt_manager,
    )


@pytest.fixture
def valid_form():
    return LoginForm(
        email=EmailAddress("User@example.com"),
        password="secret123",
    )


async def test_login_success(
    use_case, user_uow, password_hasher, jwt_manager, valid_form
):
    user = Mock()
    user.id = 42
    user.is_active = True
    user.password_hash = "hashed"

    user_uow.__aenter__.return_value.get_user_by_email.return_value = user
    password_hasher.verify.return_value = True

    token = await use_case.execute(valid_form)

    user_uow.__aenter__.return_value.get_user_by_email.assert_awaited_once_with(
        valid_form.email.value
    )
    password_hasher.verify.assert_called_once_with(
        valid_form.password, user.password_hash
    )
    jwt_manager.issue_access.assert_called_once_with(user.id)
    assert token == "access-token-123"


async def test_login_raises_if_user_not_found(
    use_case, user_uow, password_hasher, valid_form
):
    user_uow.__aenter__.return_value.get_user_by_email.return_value = None

    with pytest.raises(LoginError):
        await use_case.execute(valid_form)

    password_hasher.verify.assert_not_called()


async def test_login_raises_if_user_inactive(
    use_case, user_uow, password_hasher, valid_form
):
    user = Mock()
    user.id = 42
    user.is_active = False
    user.password_hash = "hashed"

    user_uow.__aenter__.return_value.get_user_by_email.return_value = user

    with pytest.raises(LoginError):
        await use_case.execute(valid_form)

    password_hasher.verify.assert_not_called()


async def test_login_raises_if_password_invalid(
    use_case, user_uow, password_hasher, valid_form
):
    user = Mock()
    user.id = 42
    user.is_active = True
    user.password_hash = "hashed"

    user_uow.__aenter__.return_value.get_user_by_email.return_value = user
    password_hasher.verify.return_value = False

    with pytest.raises(LoginError):
        await use_case.execute(valid_form)

    password_hasher.verify.assert_called_once_with(
        valid_form.password, user.password_hash
    )
