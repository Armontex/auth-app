import pytest
from sqlalchemy import select

from services.auth.infra.db.users.models import User
from services.auth.infra.db.users.repos import UserRepository
from services.auth.app.exc import EmailAlreadyExists, UserNotExists


@pytest.fixture
def user_repo(db):
    return UserRepository(session=db)


async def test_get_user_by_email_returns_user(user_repo, db):
    user = User(email="user@example.com", password_hash="hash")
    db.add(user)
    await db.flush()
    await db.refresh(user)

    found = await user_repo.get_user_by_email(email="user@example.com")

    assert found is not None
    assert found.id == user.id
    assert found.email == "user@example.com"


async def test_get_user_by_email_returns_none_for_inactive(user_repo, db):
    user = User(email="user@example.com", password_hash="hash", is_active=False)
    db.add(user)
    await db.flush()

    found = await user_repo.get_user_by_email(email="user@example.com")

    assert found is None


async def test_get_active_user_by_id_returns_user(user_repo, db):
    user = User(email="user@example.com", password_hash="hash", is_active=True)
    db.add(user)
    await db.flush()
    await db.refresh(user)

    found = await user_repo.get_active_user_by_id(user.id)

    assert found is not None
    assert found.id == user.id


async def test_get_active_user_by_id_returns_none_for_inactive(user_repo, db):
    user = User(email="user@example.com", password_hash="hash", is_active=False)
    db.add(user)
    await db.flush()
    await db.refresh(user)

    found = await user_repo.get_active_user_by_id(user.id)

    assert found is None


async def test_add_creates_user(user_repo, db):
    user = await user_repo.add(email="user@example.com", password_hash="hash")

    assert user.id is not None
    assert user.email == "user@example.com"
    assert user.password_hash == "hash"

    row = (await db.execute(select(User).where(User.id == user.id))).scalar_one()
    assert row.email == "user@example.com"


async def test_add_raises_email_already_exists_on_duplicate_email(user_repo, db):
    existing = User(email="user@example.com", password_hash="hash1")
    db.add(existing)
    await db.flush()

    with pytest.raises(EmailAlreadyExists):
        await user_repo.add(email="user@example.com", password_hash="hash2")


async def test_delete_user_marks_user_inactive(user_repo, db):
    user = User(email="user@example.com", password_hash="hash", is_active=True)
    db.add(user)
    await db.flush()
    await db.refresh(user)

    await user_repo.delete_user(user_id=user.id)

    assert user.is_active is False


async def test_delete_user_raises_if_user_not_exists(user_repo):
    with pytest.raises(UserNotExists):
        await user_repo.delete_user(user_id=9999)


async def test_set_email_updates_email(user_repo, db):
    user = User(email="old@example.com", password_hash="hash")
    db.add(user)
    await db.flush()
    await db.refresh(user)

    await user_repo.set_email(user, "new@example.com")
    await db.refresh(user)

    assert user.email == "new@example.com"


async def test_set_email_raises_email_already_exists_on_conflict(user_repo, db):
    user1 = User(email="first@example.com", password_hash="hash1")
    user2 = User(email="second@example.com", password_hash="hash2")
    db.add_all([user1, user2])
    await db.flush()
    await db.refresh(user2)

    with pytest.raises(EmailAlreadyExists):
        await user_repo.set_email(user2, "first@example.com")


async def test_set_password_hash_updates_hash(user_repo, db):
    user = User(email="user@example.com", password_hash="old-hash")
    db.add(user)
    await db.flush()
    await db.refresh(user)

    await user_repo.set_password_hash(user, "new-hash")

    assert user.password_hash == "new-hash"
