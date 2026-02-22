from fastapi import APIRouter, status, HTTPException, Depends, Response

from services.auth.app.usecases import LoginUseCase
from services.auth.domain.exc import ValidationError
from services.auth.app.exc import LoginError

from .schemas import LoginRequests, LoginResponse
from .deps import validate_content_type, get_login_usecase
from .mappers import map_login_request_to_form, map_token_to_response

from ...schemas import ValidationErrorResponse, LoginErrorResponse


router = APIRouter()


@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    responses={
        400: {
            "description": "Некорректные данные.",
            "content": {
                "application/json": {
                    "schema": ValidationErrorResponse.model_json_schema(),
                },
            },
        },
        401: {
            "description": "Неверные учётные данные.",
            "content": {
                "application/json": {
                    "schema": LoginErrorResponse.model_json_schema(),
                }
            },
        },
    },
    response_model=LoginResponse,
    dependencies=[Depends(validate_content_type)],
)
async def login(
    body: LoginRequests,
    response: Response,
    usecase: LoginUseCase = Depends(get_login_usecase),
):
    try:
        form = map_login_request_to_form(body)
        token = await usecase.execute(form)
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=True,
            max_age=60 * 60 * 24,
        )
        return map_token_to_response(token)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors
        ) from e
    except LoginError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=e.args[0]
        ) from e
