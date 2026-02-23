import pytest
from sqlalchemy import select

from services.rbac.infra.db.roles.models import Role
from services.rbac.infra.db.permissions.models import Permission
from services.rbac.infra.db.role_permissions.models import role_permissions
from services.rbac.infra.db.role_permissions.repos import RolePermissionsRepository


@pytest.fixture
def role_perm_repo(db):
    return RolePermissionsRepository(session=db)


async def _create_role(db, role_id: int | None = None) -> Role:
    role = Role(name=f"role-{role_id or 'x'}")
    db.add(role)
    await db.flush()
    await db.refresh(role)
    return role


async def _create_permission(
    db, perm_id: int | None = None, code: str = "PERM"
) -> Permission:
    perm = Permission(code=code)
    if perm_id is not None:
        perm.id = perm_id
    db.add(perm)
    await db.flush()
    await db.refresh(perm)
    return perm


async def test_ensure_link_inserts_when_not_exists(role_perm_repo, db):
    role = await _create_role(db)
    perm = await _create_permission(db, code="PROFILE_READ")

    await role_perm_repo.ensure_link(role.id, perm.id)

    rows = (
        await db.execute(
            select(role_permissions).where(
                role_permissions.c.role_id == role.id,
                role_permissions.c.permission_id == perm.id,
            )
        )
    ).all()
    assert len(rows) == 1


async def test_ensure_link_does_not_duplicate_existing(role_perm_repo, db):
    role = await _create_role(db)
    perm = await _create_permission(db, code="PROFILE_READ")

    await role_perm_repo.ensure_link(role.id, perm.id)
    await role_perm_repo.ensure_link(role.id, perm.id)

    rows = (
        await db.execute(
            select(role_permissions).where(
                role_permissions.c.role_id == role.id,
                role_permissions.c.permission_id == perm.id,
            )
        )
    ).all()
    assert len(rows) == 1


async def test_delete_link_removes_row_if_exists(role_perm_repo, db):
    role = await _create_role(db)
    perm = await _create_permission(db, code="PROFILE_DELETE")

    await role_perm_repo.ensure_link(role.id, perm.id)
    await role_perm_repo.delete_link(role.id, perm.id)

    rows = (
        await db.execute(
            select(role_permissions).where(
                role_permissions.c.role_id == role.id,
                role_permissions.c.permission_id == perm.id,
            )
        )
    ).all()
    assert rows == []


async def test_get_permissions_for_role_returns_all_ids(role_perm_repo, db):
    role = await _create_role(db)
    perm1 = await _create_permission(db, code="P1")
    perm2 = await _create_permission(db, code="P2")
    perm3 = await _create_permission(db, code="P3")

    await role_perm_repo.ensure_link(role.id, perm1.id)
    await role_perm_repo.ensure_link(role.id, perm2.id)
    await role_perm_repo.ensure_link(role.id, perm3.id)

    result = await role_perm_repo.get_permissions_for_role(role.id)

    assert result == {perm1.id, perm2.id, perm3.id}
