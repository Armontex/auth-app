from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)
from config.settings import settings
from common.base.db import Base

from services.auth.app.containers import AuthContainer
from services.register.app.containers import RegisterContainer
from services.profile.app.containers import ProfileContainer
from services.rbac.app.containers import RbacContainer


def create_engine() -> AsyncEngine:
    return create_async_engine(settings.postgres_url, echo=False)


def create_session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )


async def create_tables(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def create_containers(
    app: FastAPI, session_maker: async_sessionmaker[AsyncSession]
) -> None:
    app.state.auth_container = AuthContainer(session_maker=session_maker)
    app.state.profile_container = ProfileContainer(session_maker=session_maker)
    app.state.rbac_container = RbacContainer(session_maker=session_maker)
    app.state.register_container = RegisterContainer(
        session_maker=session_maker,
        password_hasher=app.state.auth_container.password_hasher,
        auth_register_factory=app.state.auth_container.register_factory,
        profile_register_factory=app.state.profile_container.register_factory,
        set_role_func=app.state.rbac_container.set_role_func,
    )


async def init_rbac(container: RbacContainer) -> None:
    usecase = container.init_rbac_usecase()
    await usecase.execute()


async def init_test_users(container: RegisterContainer) -> None:
    usecase = container.register_usecase()
    await usecase.mock_execute()


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = create_engine()
    session_maker = create_session_maker(engine)
    app.state.session_maker = session_maker

    await create_tables(engine)
    create_containers(app, session_maker)
    await init_rbac(app.state.rbac_container)

    # test
    await init_test_users(app.state.register_container)

    try:
        yield
    finally:
        await engine.dispose()
