from fastapi import APIRouter, status, Depends, Query, HTTPException
from typing import Annotated

from common.ports import IUser
from api.v1.deps import RequirePermission
from api.v1.schemas import UserNotExistsResponse

from services.auth.app.exc import UserNotExists
from services.rbac.app.exc import RoleNotFound
from services.rbac.domain.const import Permission
from services.rbac.app.usecases import (
    ReadMeRolesUseCase,
    ReadRolesUseCase,
    SetRoleUseCase,
)

from .schemas import ReadRolesResponse, SetRoleRequest
from .deps import (
    get_read_me_roles_usecase,
    get_read_roles_usecase,
    get_set_role_usecase,
)
from .mappers import map_role_name_to_role


router = APIRouter(prefix="/role", tags=["role"])


@router.get(
    path="/me",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Успешная доставка."},
        403: {"description": "Недостаточно прав."},
    },
    response_model=ReadRolesResponse,
)
async def read_me_roles(
    user: IUser = Depends(RequirePermission(Permission.ROLE_ME_READ)),
    usecase: ReadMeRolesUseCase = Depends(get_read_me_roles_usecase),
):
    return usecase.execute(user)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Успешная доставка"},
        400: {
            "description": "Такого пользователя не существует",
            "content": {
                "application/json": {
                    "schema": UserNotExistsResponse.model_json_schema()
                }
            },
        },
        403: {"description": "Недостаточно прав."},
    },
    response_model=ReadRolesResponse,
)
async def read_roles(
    user_id: Annotated[int, Query(description="ID пользователя")],
    usecase: ReadRolesUseCase = Depends(get_read_roles_usecase),
    _: IUser = Depends(RequirePermission(Permission.ROLE_READ)),
):
    try:
        return usecase.execute(user_id)
    except UserNotExists as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.args[0]
        ) from e


@router.post(
    path="/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Роль успешно добавлена."},
        400: {
            "description": "Некорректные данные.",
            "content": {
                "application/json": {"example": {"detail": "User not exists."}}
            },
        },
        403: {"description": "Недостаточно прав."},
    },
)
async def set_role(
    body: SetRoleRequest,
    set_role: SetRoleUseCase = Depends(get_set_role_usecase),
    _: IUser = Depends(RequirePermission(Permission.ROLE_SET)),
):
    try:
        role = map_role_name_to_role(body.role)
        await set_role.execute(body.user_id, role)
    except (RoleNotFound, UserNotExists) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.args[0]
        ) from e
