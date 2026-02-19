import pytest
import os
from testcontainers.redis import RedisContainer
from redis_om import get_redis_connection
from services.auth.infra.db.tokens.repos import TokenRepositoryRedis


@pytest.fixture(scope="session")
def redis_url():
    with RedisContainer(f"redis:{os.environ['REDIS_VERSION']}") as container:
        host = container.get_container_host_ip()
        port = container.get_exposed_port(6379)
        yield f"redis://{host}:{port}/0"


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
