import pytest
from unittest.mock import AsyncMock, MagicMock, call

from services.rbac.app.usecases.init_rbac import InitRbacUseCase
from services.rbac.domain.const import Permission, Role, ROLE_PERMISSIONS


@pytest.mark.asyncio
async def test_initrbac_creates_all_roles_and_permissions():
    # подготавливаем id для ролей и пермишенов
    role_ids = {r: i + 1 for i, r in enumerate(Role)}
    perm_ids = {p: i + 100 for i, p in enumerate(Permission)}

    role_repo = MagicMock()
    role_repo.upsert = AsyncMock(
        side_effect=lambda name: role_ids[next(r for r in Role if r.value == name)]
    )

    perm_repo = MagicMock()
    perm_repo.upsert = AsyncMock(
        side_effect=lambda code: perm_ids[
            next(p for p in Permission if p.value == code)
        ]
    )

    role_perms_repo = MagicMock()
    role_perms_repo.get_permissions_for_role = AsyncMock(return_value=set())
    role_perms_repo.ensure_link = AsyncMock()
    role_perms_repo.delete_link = AsyncMock()

    uow = MagicMock()
    uow.__aenter__ = AsyncMock(
        return_value=MagicMock(
            role=role_repo,
            perm=perm_repo,
            role_perms=role_perms_repo,
        )
    )
    uow.__aexit__ = AsyncMock(return_value=False)

    usecase = InitRbacUseCase(uow)
    await usecase.execute()

    # все роли из enum Role были upsert'нуты
    role_repo.upsert.assert_has_calls(
        [call(r.value) for r in Role],
        any_order=True,
    )
    assert role_repo.upsert.call_count == len(Role)

    # все пермишены из enum Permission были upsert'нуты
    perm_repo.upsert.assert_has_calls(
        [call(p.value) for p in Permission],
        any_order=True,
    )
    assert perm_repo.upsert.call_count == len(Permission)

    # ensure_link был вызван для всех пар из ROLE_PERMISSIONS
    expected_pairs = set()
    for role in Role:
        role_id = role_ids[role]
        for perm in ROLE_PERMISSIONS.get(role, set()):
            expected_pairs.add((role_id, perm_ids[perm]))

    actual_pairs = {call.args for call in role_perms_repo.ensure_link.call_args_list}
    assert actual_pairs == expected_pairs
    role_perms_repo.delete_link.assert_not_called()


@pytest.mark.asyncio
async def test_initrbac_updates_existing_permissions_diff():
    # стабильные id
    role_ids = {r: i + 1 for i, r in enumerate(Role)}
    perm_ids = {p: i + 100 for i, p in enumerate(Permission)}

    first_role = next(iter(Role))
    role_id = role_ids[first_role]
    desired_perm_ids = {perm_ids[p] for p in ROLE_PERMISSIONS[first_role]}

    # текущее состояние: не хватает одного нужного и есть один лишний
    missing_perm_id = next(iter(desired_perm_ids))
    existing_for_role = set(desired_perm_ids)
    existing_for_role.remove(missing_perm_id)
    extra_perm_id = 9999
    existing_for_role.add(extra_perm_id)

    async def get_permissions_for_role(rid: int) -> set[int]:
        if rid == role_id:
            return existing_for_role
        return set()

    role_repo = MagicMock()
    role_repo.upsert = AsyncMock(
        side_effect=lambda name: role_ids[next(r for r in Role if r.value == name)]
    )

    perm_repo = MagicMock()
    perm_repo.upsert = AsyncMock(
        side_effect=lambda code: perm_ids[
            next(p for p in Permission if p.value == code)
        ]
    )

    role_perms_repo = MagicMock()
    role_perms_repo.get_permissions_for_role = AsyncMock(
        side_effect=get_permissions_for_role
    )
    role_perms_repo.ensure_link = AsyncMock()
    role_perms_repo.delete_link = AsyncMock()

    uow = MagicMock()
    uow.__aenter__ = AsyncMock(
        return_value=MagicMock(
            role=role_repo,
            perm=perm_repo,
            role_perms=role_perms_repo,
        )
    )
    uow.__aexit__ = AsyncMock(return_value=False)

    usecase = InitRbacUseCase(uow)
    await usecase.execute()

    # должен быть добавлен missing_perm_id
    role_perms_repo.ensure_link.assert_any_call(role_id, missing_perm_id)
    # должен быть удалён extra_perm_id
    role_perms_repo.delete_link.assert_any_call(role_id, extra_perm_id)
