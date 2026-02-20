import pytest
from unittest.mock import Mock

from common.exc import RepositoryError
from services.auth.app.usecases.register import RegisterUseCase, RegisterError
from services.auth.domain.models import RegisterForm as AuthRegisterForm
from services.profile.domain.models import RegisterForm as ProfileRegisterForm, Name


@pytest.fixture
def user_form():
    return AuthRegisterForm(
        email=Mock(value="john@example.com"),
        password="secret-password",
        confirm_password="secret-password",
    )


@pytest.fixture
def profile_form():
    return ProfileRegisterForm(
        first_name=Name("John"),
        middle_name=None,
        last_name=Name("Doe"),
    )


@pytest.fixture
def usecase(register_uow, password_hasher):
    return RegisterUseCase(register_uow, password_hasher)


async def test_happy_register(
    usecase, register_uow, password_hasher, user_form, profile_form
):
    created_user = Mock(id=1, email="john@example.com")
    register_uow.user_repo.add.return_value = created_user

    result = await usecase.execute(user_form, profile_form)

    assert result is created_user

    password_hasher.hash.assert_called_once_with(user_form.password)
    register_uow.user_repo.add.assert_awaited_once_with(
        email=user_form.email.value,
        password_hash=f"hashed-{user_form.password}",  # см. конфтест: hash = "hashed-{p}"
    )
    register_uow.profile_repo.add.assert_awaited_once_with(
        user_id=created_user.id,
        first_name=profile_form.first_name.value,
        middle_name=None,
        last_name=profile_form.last_name.value,
    )
    register_uow.__aenter__.assert_awaited_once()
    register_uow.__aexit__.assert_awaited_once()


async def test_register_repository_error_wrapped(
    usecase, register_uow, password_hasher, user_form, profile_form
):
    register_uow.user_repo.add.side_effect = RepositoryError("db error")

    with pytest.raises(RegisterError) as exc_info:
        await usecase.execute(user_form, profile_form)

    assert "db error" in str(exc_info.value)
    password_hasher.hash.assert_called_once_with(user_form.password)
    register_uow.user_repo.add.assert_awaited_once()
    register_uow.__aenter__.assert_awaited_once()
    register_uow.__aexit__.assert_awaited_once()


async def test_register_calls_hash_before_repo(
    usecase, register_uow, password_hasher, user_form, profile_form
):
    created_user = Mock(id=1, email="john@example.com")
    register_uow.user_repo.add.return_value = created_user

    result = await usecase.execute(user_form, profile_form)

    assert result is created_user
    assert password_hasher.hash.call_count == 1
    assert register_uow.user_repo.add.await_count == 1
    assert register_uow.profile_repo.add.await_count == 1
    register_uow.__aenter__.assert_awaited_once()
    register_uow.__aexit__.assert_awaited_once()
