import pytest
from unittest.mock import MagicMock

from services.profile.app.usecases import ReadMeProfileUseCase


def test_execute_returns_user_profile():
    profile = MagicMock()
    user = MagicMock()
    user.profile = profile

    usecase = ReadMeProfileUseCase()

    result = usecase.execute(user)

    assert result is profile
