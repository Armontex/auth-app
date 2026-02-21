from fastapi import APIRouter, Depends, HTTPException, status

from services.auth.domain.exc import ValidationError as AuthValidationError
from services.auth.app.exc import EmailAlreadyExists
from services.auth.api.v1.schemas import (
    ValidationErrorResponse,
    EmailAlreadyExistsResponse,
)

from services.profile.domain.exc import ValidationError as ProfileValidationError
from services.profile.app.exc import ProfileAlreadyExists

from services.register.app.usecases import RegisterUseCase

from .schemas import RegisterRequests, RegisterResponse
from .deps import validate_content_type, get_register_usecase
from .mappers import (
    map_user_to_response,
    map_request_to_auth_form,
    map_request_to_profile_form,
)

router = APIRouter()


@router.post(
    path="/",
    status_code=201,
    responses={
        201: {
            "description": "Успешная регистрация",
        },
        400: {
            "description": "Некорректные данные.",
            "content": {
                "application/json": {
                    "schema": ValidationErrorResponse.model_json_schema()
                }
            },
        },
        409: {
            "description": "Пользователь с таким email уже существует.",
            "content": {
                "application/json": {
                    "schema": EmailAlreadyExistsResponse.model_json_schema()
                }
            },
        },
    },
    response_model=RegisterResponse,
    dependencies=[Depends(validate_content_type)],
)
async def register(
    body: RegisterRequests,
    usecase: RegisterUseCase = Depends(get_register_usecase),
):
    try:
        auth_form = map_request_to_auth_form(body)
        profile_form = map_request_to_profile_form(body)
        user = await usecase.execute(auth_form, profile_form)
    except (AuthValidationError, ProfileValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors
        ) from e
    except (EmailAlreadyExists, ProfileAlreadyExists) as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=e.args[0]
        ) from e

    return map_user_to_response(user)
