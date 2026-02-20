from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide
from .deps import get_bearer_token
from .mappers import map_logout_error
from ...app.usecases.logout import LogoutUseCase, LogoutError
from ...app.containers import AuthContainer

router = APIRouter(prefix="/v1/auth/", tags=["auth"])


@router.post(
    path="/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {
            "description": "Unauthorized",
            "content": {
                "application/json": {"example": {"detail": "Invalid or expired token."}}
            },
        }
    },
)
@inject
async def logout(
    token: str = Depends(get_bearer_token),
    usecase: LogoutUseCase = Depends(Provide[AuthContainer.logout_usecase]),
):
    try:
        await usecase.execute(token)
    except LogoutError as e:
        raise map_logout_error(e) from e
