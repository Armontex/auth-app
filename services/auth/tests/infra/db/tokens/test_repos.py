import pytest
import time
import uuid
from redis_om import get_redis_connection
from services.auth.infra.db.tokens.repos import TokenRepositoryRedis
from services.auth.infra.db.tokens.models import RevokedToken


@pytest.fixture(autouse=True)
def clean_redis(redis_url):
    conn = get_redis_connection(url=redis_url)
    conn.ping()
    for key in conn.keys("blacklist:*"):
        conn.delete(key)
    yield
    for key in conn.keys("blacklist:*"):
        conn.delete(key)


@pytest.fixture
def token_repo(redis_url) -> TokenRepositoryRedis:
    return TokenRepositoryRedis(redis_url)


def _now_ts() -> float:
    return time.time()


def test_revoke_token_saves_with_ttl(token_repo):
    jti = str(uuid.uuid4())
    expire = _now_ts() + 5

    token_repo.revoke_token(jti=jti, expire=expire)

    obj = RevokedToken.get(jti)
    assert obj is not None
    assert obj.jti == jti

    conn = RevokedToken.db()
    ttl = conn.ttl(obj.key())
    assert ttl > 0


def test_revoke_token_does_nothing_if_expired_in_past(token_repo):
    jti = str(uuid.uuid4())
    expire = _now_ts() - 10

    token_repo.revoke_token(jti=jti, expire=expire)

    assert token_repo.is_revoked(jti) is False


def test_is_revoked_returns_true_after_revoke(token_repo):
    jti = str(uuid.uuid4())
    expire = _now_ts() + 60

    token_repo.revoke_token(jti=jti, expire=expire)

    assert token_repo.is_revoked(jti) is True


def test_is_revoked_returns_false_for_unknown_jti(token_repo):
    jti = str(uuid.uuid4())

    assert token_repo.is_revoked(jti) is False
