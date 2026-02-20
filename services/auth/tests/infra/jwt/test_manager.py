import pytest
import jwt
from unittest.mock import AsyncMock

from datetime import datetime, timedelta, UTC

from services.auth.infra.jwt.manager import JWTManager, TokenPayload
from services.auth.infra.jwt.exc import VerifyError
from services.auth.infra.jwt.ports import ITokenRepository


SECRET_KEY = "test-secret"


@pytest.fixture
def token_repo_mock():
    repo = AsyncMock(spec=ITokenRepository)
    repo.is_revoked.return_value = False
    return repo


@pytest.fixture
def jwt_manager(token_repo_mock):
    return JWTManager(token_repo=token_repo_mock, secret_key=SECRET_KEY)


async def test_issue_access_and_verify_success(jwt_manager, token_repo_mock):
    token = jwt_manager.issue_access(user_id=123)

    payload = await jwt_manager.verify(token)

    assert isinstance(payload, TokenPayload)
    assert payload.sub == "123"
    assert isinstance(payload.jti, str)
    token_repo_mock.is_revoked.assert_awaited_once_with(payload.jti)


async def test_verify_invalid_token(jwt_manager):
    with pytest.raises(VerifyError) as exc:
        await jwt_manager.verify("not-a-jwt-token")

    assert "Invalid or expired token" in str(exc.value)


async def test_verify_expired_token(jwt_manager):
    now = datetime.now(UTC)
    exp = now - timedelta(minutes=1)

    payload = {
        "sub": 1,
        "jti": "some-jti",
        "iat": now.timestamp(),
        "exp": exp.timestamp(),
    }
    token = jwt.encode(payload, key=SECRET_KEY, algorithm=JWTManager.ALGORITHM)

    with pytest.raises(VerifyError) as exc:
        await jwt_manager.verify(token)

    assert "Invalid or expired token" in str(exc.value)


async def test_verify_revoked_token(jwt_manager, token_repo_mock):
    token = jwt_manager.issue_access(user_id=1)

    token_repo_mock.is_revoked.return_value = True

    with pytest.raises(VerifyError) as exc:
        await jwt_manager.verify(token)

    assert "Revoked token" in str(exc.value)


async def test_revoke_calls_repo(jwt_manager, token_repo_mock):
    token = jwt_manager.issue_access(user_id=1)

    await jwt_manager.revoke(token)

    token_repo_mock.revoke_token.assert_awaited_once()
    (jti, exp), _ = token_repo_mock.revoke_token.await_args
    assert isinstance(jti, str)
    assert isinstance(exp, float)
