from fastapi import APIRouter, status, HTTPException, Depends

from services.auth.app.usecases import ChangePasswordUseCase
from services.auth.app.exc import LoginError
from services.auth.domain.exc import ValidationError

from .deps import validate_content_type, get_change_password_usecase
from .schemas import ChangePasswordRequest
from .mappers import map_request_to_form
from ...schemas import ValidationErrorResponse, LoginErrorResponse

router = APIRouter()


@router.post(
    path="/change-password",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Пароль успешно изменён"},
        400: {
            "description": "Некорректные данные.",
            "content": {
                "application/json": {
                    "schema": ValidationErrorResponse.model_json_schema(),
                },
            },
        },
        401: {
            "description": "Неверные учётные данные",
            "content": {
                "application/json": {
                    "schema": LoginErrorResponse.model_json_schema(),
                },
            },
        },
    },
    dependencies=[Depends(validate_content_type)],
)
async def change_password(
    body: ChangePasswordRequest,
    usecase: ChangePasswordUseCase = Depends(get_change_password_usecase),
):
    try:
        form = map_request_to_form(body)
        await usecase.execute(form)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors
        ) from e
    except LoginError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=e.args[0]
        ) from e
