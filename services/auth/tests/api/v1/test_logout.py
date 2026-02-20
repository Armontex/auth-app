import pytest
from unittest.mock import AsyncMock

from fastapi import status

from services.auth.api.v1.deps import get_logout_usecase
from services.auth.app.usecases import LogoutUseCase, LogoutError


@pytest.fixture
def override_logout_usecase(app_for_tests):
    mock = AsyncMock(spec=LogoutUseCase)

    async def _override():
        return mock

    app_for_tests.dependency_overrides[get_logout_usecase] = _override
    yield mock
    app_for_tests.dependency_overrides.clear()


def test_logout_success(client, override_logout_usecase):

    token = "some-token"

    resp = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resp.status_code == status.HTTP_204_NO_CONTENT
    override_logout_usecase.execute.assert_awaited_once()


def test_logout_bad_token(client, override_logout_usecase):
    override_logout_usecase.execute.side_effect = LogoutError(
        "Invalid or expired token"
    )

    resp = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": "Bearer bad-token"},
    )

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED
    assert resp.json() == {"detail": "Invalid or expired token"}
