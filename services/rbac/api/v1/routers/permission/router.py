from fastapi import APIRouter, status, HTTPException, Depends, Query
from typing import Annotated

from common.ports import IUser

from api.v1.schemas import UserNotExistsResponse, TokenVerifyErrorResponse

from services.auth.app.exc import UserNotExists

from services.rbac.app.usecases import ReadPermissionsUseCase, ReadMePermissionsUseCase

from .schemas import ReadPermissionsResponse
from .deps import (
    get_read_me_perms_usecase,
    get_read_perms_usecase,
    require_permission_me_read,
    require_permission_read,
)
from .mappers import map_perms_to_response


router = APIRouter(prefix="/permission", tags=["permission"])


@router.get(
    path="/me",
    tags=["me"],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Успешная доставка."},
        400: {
            "description": "Такого пользователя не существует",
            "content": {
                "application/json": {
                    "schema": UserNotExistsResponse.model_json_schema()
                }
            },
        },
        401: {
            "description": "Токен отсутствует / невалиден / истёк",
            "content": {
                "application/json": {
                    "schema": TokenVerifyErrorResponse.model_json_schema(),
                },
            },
        },
        403: {"description": "Недостаточно прав."},
    },
    response_model=ReadPermissionsResponse,
)
async def read_me_permissions(
    user: IUser = Depends(require_permission_me_read),
    usecase: ReadMePermissionsUseCase = Depends(get_read_me_perms_usecase),
):
    try:
        return map_perms_to_response(await usecase.execute(user))
    except UserNotExists as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.args[0]
        ) from e


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
        401: {
            "description": "Токен отсутствует / невалиден / истёк",
            "content": {
                "application/json": {
                    "schema": TokenVerifyErrorResponse.model_json_schema(),
                },
            },
        },
        403: {"description": "Недостаточно прав."},
    },
    response_model=ReadPermissionsResponse,
)
async def read_permissions(
    user_id: Annotated[int, Query(description="ID пользователя")],
    usecase: ReadPermissionsUseCase = Depends(get_read_perms_usecase),
    _: IUser = Depends(require_permission_read),
):
    try:
        return map_perms_to_response(await usecase.execute(user_id))
    except UserNotExists as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.args[0]
        ) from e
