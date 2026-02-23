import pytest
from sqlalchemy import select

from services.auth.infra.db.users.models import User
from services.profile.infra.db.profiles.models import Profile
from services.profile.infra.db.profiles.repos import ProfileRepository
from services.profile.app.exc import ProfileAlreadyExists


@pytest.fixture
def profile_repo(db):
    return ProfileRepository(session=db)


async def test_add_creates_profile(profile_repo, db):
    user = User(email="user@example.com", password_hash="hash")
    db.add(user)
    await db.flush()
    await db.refresh(user)

    profile = await profile_repo.add(
        user_id=user.id,
        first_name="John",
        middle_name="M",
        last_name="Doe",
    )

    assert profile.id is not None
    assert profile.user_id == user.id
    assert profile.first_name == "John"
    assert profile.middle_name == "M"
    assert profile.last_name == "Doe"

    row = (
        await db.execute(select(Profile).where(Profile.id == profile.id))
    ).scalar_one()
    assert row.user_id == user.id
    assert row.first_name == "John"


async def test_add_raises_profile_already_exists_on_duplicate_user_id(profile_repo, db):
    user = User(email="user@example.com", password_hash="hash")
    db.add(user)
    await db.flush()
    await db.refresh(user)

    first = Profile(
        user_id=user.id,
        first_name="John",
        middle_name=None,
        last_name="Doe",
    )
    db.add(first)
    await db.flush()

    with pytest.raises(ProfileAlreadyExists):
        await profile_repo.add(
            user_id=user.id,
            first_name="Jane",
            middle_name=None,
            last_name="Smith",
        )


async def test_get_by_user_id_returns_profile(profile_repo, db):
    user = User(email="user@example.com", password_hash="hash")
    db.add(user)
    await db.flush()
    await db.refresh(user)

    profile = Profile(
        user_id=user.id,
        first_name="John",
        middle_name=None,
        last_name="Doe",
    )
    db.add(profile)
    await db.flush()
    await db.refresh(profile)

    found = await profile_repo.get_by_user_id(user.id)

    assert found is not None
    assert found.id == profile.id
    assert found.user_id == user.id


async def test_get_by_user_id_returns_none_for_unknown_user(profile_repo):
    found = await profile_repo.get_by_user_id(9999)
    assert found is None


async def test_set_first_name_updates_field(profile_repo, db):
    user = User(email="user@example.com", password_hash="hash")
    db.add(user)
    await db.flush()
    await db.refresh(user)

    profile = Profile(
        user_id=user.id,
        first_name="John",
        middle_name=None,
        last_name="Doe",
    )
    db.add(profile)
    await db.flush()
    await db.refresh(profile)

    await profile_repo.set_first_name(profile, "Jane")

    assert profile.first_name == "Jane"


async def test_set_last_name_updates_field(profile_repo, db):
    user = User(email="user@example.com", password_hash="hash")
    db.add(user)
    await db.flush()
    await db.refresh(user)

    profile = Profile(
        user_id=user.id,
        first_name="John",
        middle_name=None,
        last_name="Doe",
    )
    db.add(profile)
    await db.flush()
    await db.refresh(profile)

    await profile_repo.set_last_name(profile, "Smith")

    assert profile.last_name == "Smith"


async def test_set_middle_name_updates_field(profile_repo, db):
    user = User(email="user@example.com", password_hash="hash")
    db.add(user)
    await db.flush()
    await db.refresh(user)

    profile = Profile(
        user_id=user.id,
        first_name="John",
        middle_name=None,
        last_name="Doe",
    )
    db.add(profile)
    await db.flush()
    await db.refresh(profile)

    await profile_repo.set_middle_name(profile, "Middle")

    assert profile.middle_name == "Middle"

    await profile_repo.set_middle_name(profile, None)

    assert profile.middle_name is None
