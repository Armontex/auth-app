import pytest
from unittest.mock import AsyncMock, MagicMock

from services.profile.app.usecases.read_profile import ReadProfileUseCase
from services.profile.app.exc import ProfileNotFound


@pytest.fixture
def uow_mock():
    uow = AsyncMock()
    repos = MagicMock()
    repos.profile = AsyncMock()
    repos.profile.get_by_user_id = AsyncMock()
    uow.__aenter__.return_value = repos
    return uow


@pytest.fixture
def usecase(uow_mock):
    return ReadProfileUseCase(uow=uow_mock)


@pytest.mark.asyncio
async def test_execute_returns_profile(usecase, uow_mock):
    user_id = 10
    profile = MagicMock()
    uow_mock.__aenter__.return_value.profile.get_by_user_id.return_value = profile

    result = await usecase.execute(user_id)

    uow_mock.__aenter__.return_value.profile.get_by_user_id.assert_awaited_once_with(
        user_id
    )
    assert result is profile


@pytest.mark.asyncio
async def test_execute_raises_profile_not_found_when_missing(usecase, uow_mock):
    user_id = 999
    uow_mock.__aenter__.return_value.profile.get_by_user_id.return_value = None

    with pytest.raises(ProfileNotFound):
        await usecase.execute(user_id)
