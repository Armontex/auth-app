import pytest
from unittest.mock import AsyncMock, Mock

from services.auth.app.ports import IPasswordHasher, IUserRepository, IUser
from services.auth.app.usecases.register import RegisterUseCase, RegisterError
from services.auth.domain.models import RegisterForm
from common.exc import RepositoryError


@pytest.fixture
def user_repo() -> IUserRepository:
    repo = AsyncMock(spec=IUserRepository)
    repo.add_user = AsyncMock()
    return repo


@pytest.fixture
def password_hasher() -> IPasswordHasher:
    hasher = Mock(spec=IPasswordHasher)
    hasher.hash = Mock()
    hasher.verify = Mock()
    return hasher


@pytest.fixture
def register_form() -> RegisterForm:
    return RegisterForm(
        first_name="John",
        middle_name=None,
        last_name="Doe",
        email=Mock(value="john@example.com"),
        password="secret-password",
        confirm_password="secret-password",
    )


@pytest.mark.asyncio
async def test_happy_register(user_repo, password_hasher, register_form):
    created_user = Mock(spec=IUser)
    user_repo.add_user.return_value = created_user
    password_hasher.hash.return_value = "hashed-password"

    usecase = RegisterUseCase(user_repo, password_hasher)

    result = await usecase.execute(register_form)

    assert result is created_user

    password_hasher.hash.assert_called_once_with(register_form.password)
    user_repo.add_user.assert_awaited_once_with(
        first_name=register_form.first_name,
        middle_name=register_form.middle_name,
        last_name=register_form.last_name,
        email=register_form.email.value,
        password_hash="hashed-password",
    )


@pytest.mark.asyncio
async def test_register_repository_error_wrapped(
    user_repo, password_hasher, register_form
):
    user_repo.add_user.side_effect = RepositoryError("db error")
    password_hasher.hash.return_value = "hashed-password"

    usecase = RegisterUseCase(user_repo, password_hasher)

    with pytest.raises(RegisterError) as exc_info:
        await usecase.execute(register_form)

    assert "User with this email already exists." in str(exc_info.value)
    password_hasher.hash.assert_called_once_with(register_form.password)
    user_repo.add_user.assert_awaited_once()


@pytest.mark.asyncio
async def test_register_calls_hash_before_repo(
    user_repo, password_hasher, register_form
):
    created_user = Mock(spec=IUser)
    user_repo.add_user.return_value = created_user
    password_hasher.hash.return_value = "hashed-password"

    usecase = RegisterUseCase(user_repo, password_hasher)

    result = await usecase.execute(register_form)
    assert result is created_user

    assert password_hasher.hash.call_count == 1
    assert user_repo.add_user.await_count == 1
