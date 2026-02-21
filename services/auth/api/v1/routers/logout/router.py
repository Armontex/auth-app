from fastapi import APIRouter, status, HTTPException, Depends

from services.auth.app.usecases import LogoutUseCase
from services.auth.app.exc import TokenVerifyError

from .deps import get_logout_usecase, get_bearer_token

from ...schemas import TokenVerifyErrorResponse


router = APIRouter()


@router.post(
    path="/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Успешный logout, токен отозван"},
        401: {
            "description": "Токен отсутствует / невалиден / истёк",
            "content": {
                "application/json": {
                    "schema": TokenVerifyErrorResponse.model_json_schema(),
                },
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
    except TokenVerifyError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.args[0],
        ) from e
