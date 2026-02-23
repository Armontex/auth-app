import pytest
from sqlalchemy import select

from services.rbac.infra.db.roles.models import Role
from services.rbac.infra.db.roles.repos import RoleRepository


@pytest.fixture
def role_repo(db):
    return RoleRepository(session=db)


async def test_get_by_name_returns_role(role_repo, db):
    r = Role(name="admin")
    db.add(r)
    await db.flush()
    await db.refresh(r)

    found = await role_repo.get_by_name("admin")

    assert found is not None
    assert found.id == r.id
    assert found.name == "admin"


async def test_get_by_name_returns_none_for_unknown_name(role_repo):
    found = await role_repo.get_by_name("unknown")
    assert found is None


async def test_upsert_inserts_when_not_exists(role_repo, db):
    role_id = await role_repo.upsert("manager")

    assert isinstance(role_id, int)

    row = (await db.execute(select(Role).where(Role.id == role_id))).scalar_one()
    assert row.name == "manager"


async def test_upsert_returns_existing_id_when_already_exists(role_repo, db):
    r = Role(name="viewer")
    db.add(r)
    await db.flush()
    await db.refresh(r)

    role_id = await role_repo.upsert("viewer")

    assert role_id == r.id

    rows = (await db.execute(select(Role).where(Role.name == "viewer"))).scalars().all()
    # не создали дубль
    assert len(rows) == 1
