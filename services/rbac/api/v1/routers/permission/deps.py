from fastapi import Depends
from api.v1.deps import get_rbac_container
from services.rbac.app.usecases import ReadMePermissionsUseCase, ReadPermissionsUseCase
from services.rbac.app.containers import RbacContainer


def get_read_me_perms_usecase(
    container: RbacContainer = Depends(get_rbac_container),
) -> ReadMePermissionsUseCase:
    return container.read_me_perms_usecase()


def get_read_perms_usecase(
    container: RbacContainer = Depends(get_rbac_container),
) -> ReadPermissionsUseCase:
    return container.read_perms_usecase()
