import pytest
from sqlalchemy import select

from services.rbac.infra.db.permissions.models import Permission
from services.rbac.infra.db.permissions.repos import PermissionRepository


@pytest.fixture
def perm_repo(db):
    return PermissionRepository(session=db)


async def test_get_by_code_returns_permission(perm_repo, db):
    p = Permission(code="PROFILE_READ")
    db.add(p)
    await db.flush()
    await db.refresh(p)

    found = await perm_repo.get_by_code("PROFILE_READ")

    assert found is not None
    assert found.id == p.id
    assert found.code == "PROFILE_READ"


async def test_get_by_code_returns_none_for_unknown_code(perm_repo):
    found = await perm_repo.get_by_code("UNKNOWN_CODE")
    assert found is None


async def test_upsert_inserts_when_not_exists(perm_repo, db):
    perm_id = await perm_repo.upsert("NEW_CODE")

    assert isinstance(perm_id, int)

    row = (
        await db.execute(select(Permission).where(Permission.id == perm_id))
    ).scalar_one()
    assert row.code == "NEW_CODE"


async def test_upsert_returns_existing_id_when_already_exists(perm_repo, db):
    p = Permission(code="EXISTING")
    db.add(p)
    await db.flush()
    await db.refresh(p)

    perm_id = await perm_repo.upsert("EXISTING")

    assert perm_id == p.id

    cnt = (
        (await db.execute(select(Permission).where(Permission.code == "EXISTING")))
        .scalars()
        .all()
    )
    # не создали дубль
    assert len(cnt) == 1
