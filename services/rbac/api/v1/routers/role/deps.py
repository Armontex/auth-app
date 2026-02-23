from fastapi import Depends
from api.v1.deps import get_rbac_container
from services.rbac.app.usecases import (
    ReadMeRolesUseCase,
    ReadRolesUseCase,
    SetRoleUseCase,
)
from services.rbac.app.containers import RbacContainer


def get_read_me_roles_usecase(
    container: RbacContainer = Depends(get_rbac_container),
) -> ReadMeRolesUseCase:
    return container.read_me_roles_usecase()


def get_read_roles_usecase(
    container: RbacContainer = Depends(get_rbac_container),
) -> ReadRolesUseCase:
    return container.read_roles_usecase()


def get_set_role_usecase(
    container: RbacContainer = Depends(get_rbac_container),
) -> SetRoleUseCase:
    return container.set_role_usecase()
