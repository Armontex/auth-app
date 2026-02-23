import pytest
from unittest.mock import AsyncMock, MagicMock

from services.profile.app.usecases.update import UpdateUseCase


@pytest.fixture
def uow_mock():
    uow = AsyncMock()
    repos = MagicMock()
    repos.profile = AsyncMock()
    repos.profile.set_first_name = AsyncMock()
    repos.profile.set_last_name = AsyncMock()
    repos.profile.set_middle_name = AsyncMock()
    repos.profile.refresh = AsyncMock()
    uow.__aenter__.return_value = repos
    return uow


@pytest.fixture
def usecase(uow_mock):
    return UpdateUseCase(uow=uow_mock)


async def test_execute_updates_all_fields_when_provided(usecase, uow_mock):
    profile = MagicMock()
    user = MagicMock()
    user.profile = profile

    form = MagicMock()
    form.first_name.value = "John"
    form.last_name.value = "Doe"
    form.middle_name.value = "Middle"

    result = await usecase.execute(user, form)

    repos = uow_mock.__aenter__.return_value
    repos.profile.set_first_name.assert_awaited_once_with(profile, "John")
    repos.profile.set_last_name.assert_awaited_once_with(profile, "Doe")
    repos.profile.set_middle_name.assert_awaited_once_with(profile, "Middle")
    repos.profile.refresh.assert_awaited_once_with(profile)
    assert result is profile


async def test_execute_updates_only_present_fields(usecase, uow_mock):
    profile = MagicMock()
    user = MagicMock()
    user.profile = profile

    form = MagicMock()
    form.first_name = None
    form.last_name.value = "Doe"
    form.middle_name = None

    await usecase.execute(user, form)

    repos = uow_mock.__aenter__.return_value
    repos.profile.set_first_name.assert_not_awaited()
    repos.profile.set_middle_name.assert_not_awaited()
    repos.profile.set_last_name.assert_awaited_once_with(profile, "Doe")
    repos.profile.refresh.assert_awaited_once_with(profile)
