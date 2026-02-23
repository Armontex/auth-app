import pytest
from sqlalchemy import select

from services.auth.infra.db.users.models import User
from services.rbac.infra.db.roles.models import Role
from services.rbac.infra.db.user_roles.models import user_roles
from services.rbac.infra.db.user_roles.repos import UserRolesRepository


@pytest.fixture
def user_roles_repo(db):
    return UserRolesRepository(session=db)


async def _create_user(db, email: str = "u@example.com") -> User:
    u = User(
        email=email,
        password_hash="hashed-password",  # важно: не None
    )
    db.add(u)
    await db.flush()
    await db.refresh(u)
    return u


async def _create_role(db, name: str = "role") -> Role:
    r = Role(name=name)
    db.add(r)
    await db.flush()
    await db.refresh(r)
    return r


async def test_ensure_link_inserts_when_not_exists(user_roles_repo, db):
    user = await _create_user(db, "user1@example.com")
    role = await _create_role(db, "admin")

    await user_roles_repo.ensure_link(user.id, role.id)

    rows = (
        await db.execute(
            select(user_roles).where(
                user_roles.c.user_id == user.id,
                user_roles.c.role_id == role.id,
            )
        )
    ).all()
    assert len(rows) == 1


async def test_ensure_link_does_not_duplicate_existing(user_roles_repo, db):
    user = await _create_user(db, "user2@example.com")
    role = await _create_role(db, "manager")

    await user_roles_repo.ensure_link(user.id, role.id)
    await user_roles_repo.ensure_link(user.id, role.id)

    rows = (
        await db.execute(
            select(user_roles).where(
                user_roles.c.user_id == user.id,
                user_roles.c.role_id == role.id,
            )
        )
    ).all()
    assert len(rows) == 1
