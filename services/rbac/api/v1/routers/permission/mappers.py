from common.ports import IPermission
from .schemas import ReadPermissionsResponse


def map_perms_to_response(perms: set[IPermission]) -> ReadPermissionsResponse:
    return ReadPermissionsResponse(permissions=[p.code for p in perms])
