import pytest
import os

from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from common.base.db import Base

import services.rbac.infra.db.user_roles.models
import services.rbac.infra.db.role_permissions.models
import services.auth.infra.db.users.models
import services.profile.infra.db.profiles.models
import services.rbac.infra.db.roles.models
import services.rbac.infra.db.permissions.models


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer(f"postgres:{os.environ['POSTGRES_VERSION']}") as postgres:
        yield postgres


@pytest.fixture
async def db_engine(postgres_container):
    async_url = postgres_container.get_connection_url(driver="asyncpg")
    engine = create_async_engine(async_url, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
def SessionLocal(db_engine):
    return async_sessionmaker(
        bind=db_engine,
        class_=AsyncSession,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )


@pytest.fixture
async def db(SessionLocal):
    async with SessionLocal() as session:
        yield session


@pytest.fixture(scope="session")
def redis_url():
    with RedisContainer(f"redis:{os.environ['REDIS_VERSION']}") as container:
        host = container.get_container_host_ip()
        port = container.get_exposed_port(6379)
        yield f"redis://{host}:{port}/0"
