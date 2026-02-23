from fastapi import APIRouter, status, Depends, HTTPException

from common.ports import IUser
from api.v1.schemas import TokenVerifyErrorResponse

from services.profile.app.usecases import UpdateUseCase

from .deps import get_update_usecase, require_profile_me_update
from .mappers import map_profile_to_response, map_request_to_form
from .schemas import UpdateResponse, UpdateRequest

from ...deps import validate_content_type
from ...schemas import ValidationErrorResponse


from services.profile.domain.exc import ValidationError


router = APIRouter()


@router.put(
    path="/me",
    tags=["me"],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Данные успешно изменены"},
        400: {
            "description": "Некорректные данные.",
            "content": {
                "application/json": {
                    "schema": ValidationErrorResponse.model_json_schema()
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
        403: {
            "description": "Недостаточно прав",
        },
    },
    response_model=UpdateResponse,
    dependencies=[Depends(validate_content_type)],
)
async def update_profile(
    body: UpdateRequest,
    user: IUser = Depends(require_profile_me_update),
    usecase: UpdateUseCase = Depends(get_update_usecase),
):
    try:
        form = map_request_to_form(body)
        profile = await usecase.execute(user, form)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors
        ) from e

    return map_profile_to_response(profile)
