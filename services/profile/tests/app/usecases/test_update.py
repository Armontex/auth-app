import pytest
from unittest.mock import AsyncMock, MagicMock

from services.profile.app.usecases.update import UpdateUseCase


@pytest.fixture
def uow_mock():
    uow = AsyncMock()
    repos = MagicMock()
    repos.profile = MagicMock()

    repos.profile.get_by_user_id = AsyncMock()
    repos.profile.set_first_name = AsyncMock()
    repos.profile.set_last_name = AsyncMock()
    repos.profile.set_middle_name = AsyncMock()
    repos.profile.refresh = AsyncMock()

    uow.__aenter__.return_value = repos
    uow.__aexit__.return_value = False
    return uow


@pytest.fixture
def usecase(uow_mock):
    return UpdateUseCase(uow=uow_mock)


@pytest.mark.asyncio
async def test_execute_updates_all_fields_when_provided(usecase, uow_mock):
    user = MagicMock()
    user.id = 123

    profile_from_repo = MagicMock()

    form = MagicMock()
    form.first_name.value = "John"
    form.last_name.value = "Doe"
    form.middle_name.value = "Middle"

    repos = uow_mock.__aenter__.return_value
    repos.profile.get_by_user_id.return_value = profile_from_repo

    result = await usecase.execute(user, form)

    repos.profile.get_by_user_id.assert_awaited_once_with(user.id)
    repos.profile.set_first_name.assert_awaited_once_with(profile_from_repo, "John")
    repos.profile.set_last_name.assert_awaited_once_with(profile_from_repo, "Doe")
    repos.profile.set_middle_name.assert_awaited_once_with(profile_from_repo, "Middle")
    assert result is profile_from_repo


@pytest.mark.asyncio
async def test_execute_updates_only_present_fields(usecase, uow_mock):
    user = MagicMock()
    user.id = 123

    profile_from_repo = MagicMock()

    form = MagicMock()
    form.first_name = None
    form.last_name.value = "Doe"
    form.middle_name = None

    repos = uow_mock.__aenter__.return_value
    repos.profile.get_by_user_id.return_value = profile_from_repo

    await usecase.execute(user, form)

    repos.profile.get_by_user_id.assert_awaited_once_with(user.id)
    repos.profile.set_first_name.assert_not_awaited()
    repos.profile.set_middle_name.assert_not_awaited()
    repos.profile.set_last_name.assert_awaited_once_with(profile_from_repo, "Doe")
