import pytest
from unittest.mock import AsyncMock, MagicMock

from services.profile.app.usecases import ReadMeProfileUseCase, ReadProfileUseCase


async def test_execute_returns_user_profile():
    profile = MagicMock()
    user = MagicMock()
    user.id = 123

    read_profile_uc = AsyncMock(spec=ReadProfileUseCase)
    read_profile_uc.execute = AsyncMock(return_value=profile)

    usecase = ReadMeProfileUseCase(read_profile=read_profile_uc)

    result = await usecase.execute(user)

    read_profile_uc.execute.assert_awaited_once_with(123)
    assert result is profile
