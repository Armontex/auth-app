import pytest
from unittest.mock import AsyncMock

from fastapi import status

from services.auth.api.v1.deps import get_delete_user_usecase
from services.auth.app.usecases import (
    DeleteUserError,
    DeleteUserNotExistsError,
    DeleteUserUseCase,
)


@pytest.fixture
def override_delete_user_usecase(app_for_tests):
    mock = AsyncMock(spec=DeleteUserUseCase)

    async def _override():
        return mock

    app_for_tests.dependency_overrides[get_delete_user_usecase] = _override
    yield mock
    app_for_tests.dependency_overrides.clear()


def test_delete_user_success(client, override_delete_user_usecase):

    resp = client.delete(
        "/api/v1/auth",
        headers={"Authorization": "Bearer some-token"},
    )

    assert resp.status_code == status.HTTP_204_NO_CONTENT
    override_delete_user_usecase.execute.assert_awaited_once()


def test_delete_user_bad_token(client, override_delete_user_usecase):
    override_delete_user_usecase.execute.side_effect = DeleteUserError(
        "Invalid or expired token"
    )

    resp = client.delete(
        "/api/v1/auth",
        headers={"Authorization": "Bearer bad-token"},
    )

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED
    assert resp.json() == {"detail": "Invalid or expired token"}


def test_delete_user_not_found(client, override_delete_user_usecase):
    override_delete_user_usecase.execute.side_effect = DeleteUserNotExistsError(
        "This user does not exist"
    )

    resp = client.delete(
        "/api/v1/auth",
        headers={"Authorization": "Bearer deleted-user-token"},
    )

    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert resp.json() == {"detail": "This user does not exist"}
