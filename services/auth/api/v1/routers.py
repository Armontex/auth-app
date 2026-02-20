from fastapi import APIRouter, Depends, status, HTTPException
from .deps import (
    get_bearer_token,
    validate_content_type,
    get_register_usecase,
    get_logout_usecase,
    get_delete_user_usecase,
    get_login_usecase,
)
from .mappers import (
    map_register_request_to_form,
    map_user_to_response,
    map_login_request_to_form,
    map_token_to_response,
)
from .schemas import RegisterRequests, LoginRequests, RegisterResponse, LoginResponse
from ...app.usecases import (
    LogoutUseCase,
    LogoutError,
    RegisterUseCase,
    RegisterError,
    LoginUseCase,
    LoginError,
    DeleteUserUseCase,
    DeleteUserError,
    DeleteUserNotExistsError,
)
from ...domain.exc import DomainValidationError


router = APIRouter(prefix="/auth", tags=["auth"])


@router.delete(
    path="",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Пользователь успешно удалён, токен отозван"},
        401: {
            "description": "Токен отсутствует / невалиден / истёк",
            "content": {
                "application/json": {"example": {"detail": "Invalid or expired token."}}
            },
        },
        404: {
            "description": "Пользователь не существует",
            "content": {
                "application/json": {"example": {"detail": "This user does not exist"}}
            },
        },
    },
)
async def delete_user(
    token: str = Depends(get_bearer_token),
    usecase: DeleteUserUseCase = Depends(get_delete_user_usecase),
):
    try:
        await usecase.execute(token)
    except DeleteUserNotExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.args[0]
        ) from e
    except DeleteUserError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=e.args[0]
        ) from e


@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Успешная авторизация",
            "content": {"application/json": {"example": {"access_token": "<token>"}}},
        },
        400: {
            "description": "Ошибки валидации",
            "content": {
                "application/json": {"example": {"email": ["This field is required."]}}
            },
        },
        401: {
            "description": "Неверные учётные данные.",
            "content": {
                "application/json": {"example": {"detail": "Invalid credentials."}}
            },
        },
    },
    response_model=LoginResponse,
    dependencies=[Depends(validate_content_type)],
)
async def login(
    body: LoginRequests,
    usecase: LoginUseCase = Depends(get_login_usecase),
):
    try:
        form = map_login_request_to_form(body)
        token = await usecase.execute(form)
    except DomainValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors
        ) from e
    except LoginError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=e.args[0]
        ) from e

    return map_token_to_response(token)


@router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "Успешная регистрация",
            "content": {
                "application/json": {"example": {"id": 1, "email": "ivan@example.com"}}
            },
        },
        400: {
            "description": "Ошибки валидации",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "email": ["Enter a valid email address."],
                            "password": ["Passwords do not match."],
                        }
                    }
                }
            },
        },
        409: {
            "description": "Пользователь с таким `email` уже существует",
            "content": {
                "application/json": {
                    "example": {"detail": "User with this email already exists."}
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
        form = map_register_request_to_form(body)
        user = await usecase.execute(form)
    except DomainValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors
        ) from e
    except RegisterError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=e.args[0]
        ) from e

    return map_user_to_response(user)


@router.post(
    path="/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Успешный logout"},
        401: {
            "description": "Токен отсутствует / невалиден / истёк",
            "content": {
                "application/json": {"example": {"detail": "Invalid or expired token."}}
            },
        },
    },
)
async def logout(
    token: str = Depends(get_bearer_token),
    usecase: LogoutUseCase = Depends(get_logout_usecase),
):
    try:
        await usecase.execute(token)
    except LogoutError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.args[0],
        ) from e
