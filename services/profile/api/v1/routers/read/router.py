from fastapi import APIRouter, status, Depends, Query, HTTPException
from typing import Annotated

from common.ports import IUser
from api.v1.schemas import TokenVerifyErrorResponse

from services.profile.app.usecases import ReadMeProfileUseCase, ReadProfileUseCase
from services.profile.app.exc import ProfileNotFound

from .schemas import ProfileResponse
from .deps import (
    get_read_me_prof_usecase,
    get_read_prof_usecase,
    require_profile_me_read,
    require_profile_read,
)
from .mappers import map_prof_to_response


router = APIRouter()


@router.get(
    path="/me",
    tags=["me"],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Успешная доставка."},
        400: {
            "description": "Некорректные данные.",
            "content": {
                "application/json": {"example": {"detail": "Profile not exists."}}
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
    response_model=ProfileResponse,
)
async def read_me_profile(
    user: IUser = Depends(require_profile_me_read),
    usecase: ReadMeProfileUseCase = Depends(get_read_me_prof_usecase),
):
    try:
        profile = await usecase.execute(user)
        return map_prof_to_response(profile)
    except ProfileNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.args[0]
        ) from e


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Успешная доставка."},
        400: {
            "description": "Некорректные данные.",
            "content": {
                "application/json": {"example": {"detail": "Profile not exists."}}
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
    response_model=ProfileResponse,
)
async def read_profile(
    user_id: Annotated[int, Query(description="ID пользователя")],
    usecase: ReadProfileUseCase = Depends(get_read_prof_usecase),
    _: IUser = Depends(require_profile_read),
):
    try:
        profile = await usecase.execute(user_id)
        return map_prof_to_response(profile)
    except ProfileNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.args[0]
        ) from e
