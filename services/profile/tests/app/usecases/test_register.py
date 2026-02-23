import pytest
from unittest.mock import AsyncMock, MagicMock

from services.profile.app.usecases.register import RegisterUseCase


@pytest.fixture
def repo_mock():
    repo = AsyncMock()
    repo.add = AsyncMock()
    return repo


@pytest.fixture
def usecase(repo_mock):
    return RegisterUseCase(repo=repo_mock)


async def test_execute_calls_repo_add_with_all_names(usecase, repo_mock):
    form = MagicMock()
    form.first_name.value = "John"
    form.middle_name.value = "Middle"
    form.last_name.value = "Doe"

    await usecase.execute(user_id=1, form=form)

    repo_mock.add.assert_awaited_once_with(
        user_id=1,
        first_name="John",
        middle_name="Middle",
        last_name="Doe",
    )


async def test_execute_passes_none_when_middle_name_absent(usecase, repo_mock):
    form = MagicMock()
    form.first_name.value = "John"
    form.middle_name = None
    form.last_name.value = "Doe"

    await usecase.execute(user_id=2, form=form)

    repo_mock.add.assert_awaited_once_with(
        user_id=2,
        first_name="John",
        middle_name=None,
        last_name="Doe",
    )
