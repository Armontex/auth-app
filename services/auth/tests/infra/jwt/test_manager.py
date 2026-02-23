import jwt
import pytest
from datetime import datetime, timedelta, UTC
from unittest.mock import AsyncMock, Mock

from services.auth.infra.jwt.manager import JWTManager, TokenPayload
from services.auth.app.exc import TokenVerifyError


SECRET_KEY = "test-secret-key"


@pytest.fixture
def token_repo_mock():
    repo = Mock()
    repo.is_revoked = AsyncMock(return_value=False)
    repo.revoke_token = AsyncMock()
    return repo


@pytest.fixture
def jwt_manager(token_repo_mock):
    return JWTManager(token_repo=token_repo_mock, secret_key=SECRET_KEY)


def test_issue_access_creates_valid_token(jwt_manager):
    token = jwt_manager.issue_access(user_id=123)

    assert isinstance(token, str)

    decoded = jwt.decode(token, SECRET_KEY, algorithms=[JWTManager.ALGORITHM])
    assert decoded["sub"] == "123"
    assert "jti" in decoded
    assert "iat" in decoded
    assert "exp" in decoded
    assert decoded["exp"] > decoded["iat"]


async def test_verify_returns_token_payload(jwt_manager, token_repo_mock):
    token = jwt_manager.issue_access(user_id=42)

    payload = await jwt_manager.verify(token)

    assert isinstance(payload, TokenPayload)
    assert payload.sub == "42"
    token_repo_mock.is_revoked.assert_awaited_once_with(payload.jti)


async def test_verify_raises_on_invalid_signature(jwt_manager, token_repo_mock):
    token = jwt_manager.issue_access(user_id=1)
    bad_token = token[:-1] + ("a" if token[-1] != "a" else "b")

    with pytest.raises(TokenVerifyError) as exc_info:
        await jwt_manager.verify(bad_token)

    assert "Invalid or expired token" in str(exc_info.value)
    token_repo_mock.is_revoked.assert_not_awaited()


async def test_verify_raises_on_revoked_token(jwt_manager, token_repo_mock):
    token = jwt_manager.issue_access(user_id=1)

    decoded = jwt.decode(token, SECRET_KEY, algorithms=[JWTManager.ALGORITHM])
    jti = decoded["jti"]

    token_repo_mock.is_revoked.return_value = True

    with pytest.raises(TokenVerifyError) as exc_info:
        await jwt_manager.verify(token)

    assert "Revoked token" in str(exc_info.value)
    token_repo_mock.is_revoked.assert_awaited_once_with(jti)


async def test_revoke_calls_repo_with_jti_and_exp(jwt_manager, token_repo_mock):
    token = jwt_manager.issue_access(user_id=7)

    await jwt_manager.revoke(token)

    decoded = jwt.decode(token, SECRET_KEY, algorithms=[JWTManager.ALGORITHM])
    jti = decoded["jti"]
    exp = decoded["exp"]

    token_repo_mock.revoke_token.assert_awaited_once_with(jti, exp)


async def test_verify_raises_on_expired_token(token_repo_mock):
    manager = JWTManager(token_repo=token_repo_mock, secret_key=SECRET_KEY)

    now = datetime.now(UTC)
    exp = now - timedelta(minutes=1)

    payload = {
        "sub": "1",
        "jti": "expired-jti",
        "iat": now.timestamp(),
        "exp": exp.timestamp(),
    }
    token = jwt.encode(payload, key=SECRET_KEY, algorithm=JWTManager.ALGORITHM)

    with pytest.raises(TokenVerifyError) as exc_info:
        await manager.verify(token)

    assert "Invalid or expired token" in str(exc_info.value)
    token_repo_mock.is_revoked.assert_not_awaited()
