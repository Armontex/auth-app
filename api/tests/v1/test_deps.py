import pytest
from unittest.mock import AsyncMock, MagicMock

from fastapi import status

from api.v1.deps import (
    get_bearer_token,
    validate_content_type,
    RequirePermission,
)
from services.auth.app.containers import AuthorizeUseCase


def test_get_bearer_token_missing(client):
    resp = client.get(
        "/api/v1/register/"
    )
    with pytest.raises(Exception) as exc:
        get_bearer_token(None)
    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED # type: ignore
    assert exc.value.detail == "Authentication credentials were not provided."  # type: ignore


def test_get_bearer_token_invalid_format():
    with pytest.raises(Exception) as exc:
        get_bearer_token("invalid")
    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED  # type: ignore
    assert exc.value.detail == "Invalid or expired token."  # type: ignore


def test_get_bearer_token_wrong_scheme():
    with pytest.raises(Exception) as exc:
        get_bearer_token("Basic token")
    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED  # type: ignore
    assert exc.value.detail == "Invalid or expired token."  # type: ignore


def test_get_bearer_token_ok():
    token = get_bearer_token("Bearer abc123")
    assert token == "abc123"


def test_validate_content_type_ok():
    assert validate_content_type("application/json") is None


def test_validate_content_type_wrong():
    with pytest.raises(Exception) as exc:
        validate_content_type("text/plain")
    assert exc.value.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE  # type: ignore
    assert exc.value.detail == "Content-Type must be application/json"  # type: ignore


@pytest.mark.asyncio
async def test_require_permission_forbidden(monkeypatch):
    user = MagicMock()
    user.roles = []

    uc = AsyncMock(spec=AuthorizeUseCase)
    uc.execute = AsyncMock(return_value=user)

    async def fake_get_authorize_usecase():
        return uc

    from api.v1 import deps as deps_module

    monkeypatch.setattr(
        deps_module, "get_authorize_usecase", fake_get_authorize_usecase
    )

    from services.rbac.domain.const import Permission

    dep = RequirePermission(Permission.PERMISSION_ME_READ)

    with pytest.raises(Exception) as exc:
        await dep(token="jwt-token", usecase=uc)

    assert exc.value.status_code == status.HTTP_403_FORBIDDEN  # type: ignore


@pytest.mark.asyncio
async def test_require_permission_ok(monkeypatch):
    from services.rbac.domain.const import Permission

    perm = MagicMock()
    perm.code = Permission.PERMISSION_ME_READ.value
    role = MagicMock()
    role.permissions = [perm]
    user = MagicMock()
    user.roles = [role]

    uc = AsyncMock(spec=AuthorizeUseCase)
    uc.execute = AsyncMock(return_value=user)

    dep = RequirePermission(Permission.PERMISSION_ME_READ)

    result = await dep(token="jwt-token", usecase=uc)

    uc.execute.assert_awaited_once_with("jwt-token")
    assert result is user
