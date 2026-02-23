import pytest
from unittest.mock import AsyncMock, MagicMock, Mock

from services.auth.app.usecases.login import LoginUseCase
from services.auth.app.exc import LoginError


@pytest.fixture
def uow_mock():
    uow = AsyncMock()
    repos = MagicMock()
    repos.user = AsyncMock()
    repos.user.get_user_by_email = AsyncMock()
    uow.__aenter__.return_value = repos
    return uow


@pytest.fixture
def hasher_mock():
    hasher = Mock()
    hasher.verify = Mock()
    return hasher


@pytest.fixture
def jwt_mock():
    jwt = Mock()
    jwt.issue_access = Mock()
    return jwt


@pytest.fixture
def usecase(uow_mock, hasher_mock, jwt_mock):
    return LoginUseCase(
        uow=uow_mock,
        password_hasher=hasher_mock,
        jwt_manager=jwt_mock,
    )



async def test_authenticate_success(usecase, uow_mock, hasher_mock):
    form = MagicMock()
    form.email.value = "user@example.com"
    form.password = "plain"

    user = MagicMock()
    user.is_active = True
    user.password_hash = "hashed"

    uow_mock.__aenter__.return_value.user.get_user_by_email.return_value = user
    hasher_mock.verify.return_value = True

    result = await usecase.authenticate(form)

    uow_mock.__aenter__.return_value.user.get_user_by_email.assert_awaited_once_with(
        "user@example.com"
    )
    hasher_mock.verify.assert_called_once_with("plain", "hashed")
    assert result is user



@pytest.mark.parametrize(
    "user_exists, is_active, password_ok",
    [
        (False, False, False),
        (True, False, True),
        (True, True, False),
    ],
    ids=["no-user", "inactive-user", "bad-password"],
)
async def test_authenticate_raises_login_error(
    usecase, uow_mock, hasher_mock, user_exists, is_active, password_ok
):
    form = MagicMock()
    form.email.value = "user@example.com"
    form.password = "plain"

    if user_exists:
        user = MagicMock()
        user.is_active = is_active
        user.password_hash = "hashed"
        uow_mock.__aenter__.return_value.user.get_user_by_email.return_value = user
    else:
        uow_mock.__aenter__.return_value.user.get_user_by_email.return_value = None

    hasher_mock.verify.return_value = password_ok

    with pytest.raises(LoginError):
        await usecase.authenticate(form)



async def test_execute_returns_access_token(usecase, uow_mock, hasher_mock, jwt_mock):
    form = MagicMock()
    form.email.value = "user@example.com"
    form.password = "plain"

    user = MagicMock()
    user.is_active = True
    user.password_hash = "hashed"
    user.id = 123

    uow_mock.__aenter__.return_value.user.get_user_by_email.return_value = user
    hasher_mock.verify.return_value = True
    jwt_mock.issue_access.return_value = "access-token"

    token = await usecase.execute(form)

    jwt_mock.issue_access.assert_called_once_with(123)
    assert token == "access-token"
