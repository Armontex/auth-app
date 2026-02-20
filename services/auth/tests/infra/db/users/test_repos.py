import pytest
from sqlalchemy import select

from services.auth.infra.db.users.models import User
from services.auth.infra.db.users.repos import UserRepository
from common.exc import RepositoryError


@pytest.fixture
def user_repo(db):
    return UserRepository(db)


async def _create_user(
    session,
    *,
    email: str = "user@example.com",
    is_active: bool = True,
    password_hash: str = "hashed",
) -> User:
    user = User(
        email=email,
        is_active=is_active,
        password_hash=password_hash,
    )
    session.add(user)
    await session.flush()
    await session.refresh(user)
    return user


# ==== get_user_by_email ====


async def test_get_user_by_email_returns_user_when_exists(user_repo, db):
    created = await _create_user(db, email="test@example.com", is_active=True)

    result = await user_repo.get_user_by_email("test@example.com")

    assert result is not None
    assert result.id == created.id
    assert result.email == "test@example.com"


async def test_get_user_by_email_returns_none_when_not_exists(user_repo):
    result = await user_repo.get_user_by_email("nope@example.com")
    assert result is None


async def test_get_user_by_email_ignores_inactive_by_default(user_repo, db):
    await _create_user(db, email="inactive@example.com", is_active=False)

    result = await user_repo.get_user_by_email("inactive@example.com")

    assert result is None


async def test_get_user_by_email_can_search_inactive(user_repo, db):
    created = await _create_user(db, email="inactive@example.com", is_active=False)

    result = await user_repo.get_user_by_email(
        "inactive@example.com",
        is_active=False,
    )

    assert result is not None
    assert result.id == created.id
    assert result.is_active is False


# ==== add_user ====


async def test_add_user_persists_and_returns_user(user_repo: UserRepository, db):
    user = await user_repo.add(
        email="john@example.com",
        password_hash="hashed",
    )

    assert user.id is not None
    assert user.email == "john@example.com"

    stmt = select(User).where(User.id == user.id)
    result = await db.execute(stmt)
    from_db = result.scalars().first()
    assert from_db is not None
    assert from_db.email == "john@example.com"
    assert from_db.is_active is True


async def test_add_user_raises_on_duplicate_active_email(user_repo, db):
    await _create_user(db, email="dup@example.com", is_active=True)

    with pytest.raises(RepositoryError):
        await user_repo.add(
            email="dup@example.com",
            password_hash="hashed2",
        )


async def test_add_user_allows_same_email_for_inactive(user_repo, db):
    await _create_user(db, email="same@example.com", is_active=False)

    user = await user_repo.add(
        email="same@example.com",
        password_hash="hashed",
    )

    assert user.email == "same@example.com"
    assert user.is_active is True


# ==== delete_user ====


async def test_delete_user_sets_is_active_false(user_repo, db):
    user = await _create_user(db, email="del@example.com", is_active=True)

    await user_repo.delete_user(user.id)

    stmt = select(User).where(User.id == user.id)
    result = await db.execute(stmt)
    from_db = result.scalars().first()

    assert from_db is not None
    assert from_db.is_active is False


async def test_delete_user_is_idempotent_for_inactive(user_repo, db):
    user = await _create_user(db, email="inactive_del@example.com")

    await user_repo.delete_user(user.id)

    stmt = select(User).where(User.id == user.id)
    result = await db.execute(stmt)
    from_db = result.scalars().first()

    assert from_db is not None
    assert from_db.is_active is False


async def test_delete_user_does_not_affect_other_users(user_repo, db):
    user1 = await _create_user(db, email="u1@example.com", is_active=True)
    user2 = await _create_user(db, email="u2@example.com", is_active=True)

    await user_repo.delete_user(user1.id)

    stmt = select(User).where(User.id == user2.id)
    result = await db.execute(stmt)
    other = result.scalars().first()

    assert other is not None
    assert other.is_active is True
