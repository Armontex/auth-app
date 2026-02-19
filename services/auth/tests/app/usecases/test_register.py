import pytest
from unittest.mock import Mock

from services.auth.app.usecases.register import RegisterUseCase, RegisterError
from services.auth.domain.models import RegisterForm
from common.exc import RepositoryError


@pytest.fixture
def register_form():
    return RegisterForm(
        first_name="John",
        middle_name=None,
        last_name="Doe",
        email=Mock(value="john@example.com"),
        password="secret-password",
        confirm_password="secret-password",
    )


@pytest.fixture
def usecase(user_uow, password_hasher):
    return RegisterUseCase(user_uow, password_hasher)


async def test_happy_register(
    usecase, user_uow, user_repo, password_hasher, register_form
):
    created_user = Mock()
    user_repo.add_user.return_value = created_user
    password_hasher.hash.return_value = "hashed-password"

    result = await usecase.execute(register_form)

    assert result is created_user

    password_hasher.hash.assert_called_once_with(register_form.password)
    user_repo.add_user.assert_awaited_once_with(
        first_name=register_form.first_name,
        middle_name=register_form.middle_name,
        last_name=register_form.last_name,
        email=register_form.email.value,
        password_hash="hashed-secret-password",
    )
    user_uow.__aenter__.assert_awaited_once()
    user_uow.__aexit__.assert_awaited_once()


async def test_register_repository_error_wrapped(
    usecase, user_uow, user_repo, password_hasher, register_form
):
    user_repo.add_user.side_effect = RepositoryError("db error")
    password_hasher.hash.return_value = "hashed-password"

    with pytest.raises(RegisterError) as exc_info:
        await usecase.execute(register_form)

    assert "User with this email already exists." in str(exc_info.value)
    password_hasher.hash.assert_called_once_with(register_form.password)
    user_repo.add_user.assert_awaited_once()
    user_uow.__aenter__.assert_awaited_once()
    user_uow.__aexit__.assert_awaited_once()


async def test_register_calls_hash_before_repo(
    usecase, user_uow, user_repo, password_hasher, register_form
):
    created_user = Mock()
    user_repo.add_user.return_value = created_user
    password_hasher.hash.return_value = "hashed-password"

    result = await usecase.execute(register_form)

    assert result is created_user
    assert password_hasher.hash.call_count == 1
    assert user_repo.add_user.await_count == 1
    user_uow.__aenter__.assert_awaited_once()
    user_uow.__aexit__.assert_awaited_once()
