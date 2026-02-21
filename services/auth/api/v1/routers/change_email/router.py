from fastapi import status, HTTPException, Depends

from services.auth.app.usecases import ChangeEmailUseCase
from services.auth.app.exc import LoginError
from services.auth.domain.exc import ValidationError

from .schemas import ChangeEmailRequest
from .deps import get_change_email_usecase, validate_content_type
from .mappers import map_request_to_form

from .. import router

from ...schemas import ValidationErrorResponse, LoginErrorResponse


@router.post(
    path="/change-email",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Email успешно изменён"},
        400: {
            "description": "Ошибки валидации",
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
async def change_email(
    body: ChangeEmailRequest,
    usecase: ChangeEmailUseCase = Depends(get_change_email_usecase),
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
