from fastapi import APIRouter, status, Depends, HTTPException

from .deps import get_update_usecase
from .mappers import map_profile_to_response, map_request_to_form
from .schemas import UpdateResponse, UpdateRequest
from common.ports import IUser
from services.profile.app.usecases import UpdateUseCase
from services.rbac.domain.const import Permission
from ...deps import RequirePermission, validate_content_type
from ...schemas import ValidationErrorResponse


from services.profile.domain.exc import ValidationError


router = APIRouter(prefix="/me", tags=["me"])


@router.put(
    path="/",
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
        403: {
            "description": "Недостаточно прав",
        },
    },
    response_model=UpdateResponse,
    dependencies=[Depends(validate_content_type)],
)
async def update(
    body: UpdateRequest,
    user: IUser = Depends(RequirePermission(Permission.PROFILE_ME_UPDATE)),
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
