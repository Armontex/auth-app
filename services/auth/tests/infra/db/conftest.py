import pytest
import os
from testcontainers.postgres import PostgresContainer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from common.base.db import Base


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
