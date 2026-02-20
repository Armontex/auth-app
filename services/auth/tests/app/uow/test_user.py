import pytest
from unittest.mock import AsyncMock, Mock

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from services.auth.app.uow.user import UserUoW
from services.auth.infra.db.users.repos import UserRepository


@pytest.fixture
def session():
    s = AsyncMock(spec=AsyncSession)
    s.commit = AsyncMock()
    s.rollback = AsyncMock()
    s.close = AsyncMock()
    return s


@pytest.fixture
def session_factory(session):
    factory = Mock(spec=async_sessionmaker)
    factory.return_value = session
    return factory


@pytest.mark.asyncio
async def test_uow_enters_with_user_repository(session_factory, session):
    uow = UserUoW(session_factory=session_factory)

    async with uow as repo:
        assert isinstance(repo, UserRepository)
        assert repo._session is session

    session_factory.assert_called_once_with()
    session.commit.assert_awaited_once()
    session.close.assert_awaited_once()
    session.rollback.assert_not_awaited()


@pytest.mark.asyncio
async def test_uow_rolls_back_on_error(session_factory, session):
    uow = UserUoW(session_factory=session_factory)

    class TestError(Exception):
        pass

    with pytest.raises(TestError):
        async with uow as repo:
            assert isinstance(repo, UserRepository)
            raise TestError()

    session_factory.assert_called_once_with()
    session.rollback.assert_awaited_once()
    session.commit.assert_not_awaited()
    session.close.assert_awaited_once()
