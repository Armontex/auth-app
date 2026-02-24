from .deps import RequirePermission
from fastapi import APIRouter, Depends, status
from services.rbac.domain.const import Permission
from common.ports import IUser


FAKE_RESOURCES = [
    {"id": 1, "name": "Secret Document", "owner_id": 1},
    {"id": 2, "name": "Public Document", "owner_id": 2},
]

router = APIRouter()


@router.get(
    path="/resources",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "OK"},
        401: {"description": "Некорректные учётные данные."},
        403: {"description": "Недостаточно прав."},
    },
)
async def list_resources(
    _: IUser = Depends(RequirePermission(Permission.RESOURCES)),
):
    return FAKE_RESOURCES
