from fastapi import Depends
from common.ports import IUser
from api.v1.deps import get_rbac_container, RequirePermission
from services.rbac.domain.const import Permission
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


def require_permission_me_read(
    user: IUser = Depends(RequirePermission(Permission.PERMISSION_ME_READ)),
) -> IUser:
    return user


def require_permission_read(
    user: IUser = Depends(RequirePermission(Permission.PERMISSION_READ)),
) -> IUser:
    return user
