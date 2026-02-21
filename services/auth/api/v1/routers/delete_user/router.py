from fastapi import status, HTTPException, Depends

from services.auth.app.usecases import DeleteUserUseCase
from services.auth.app.exc import UserNotExists, TokenVerifyError

from .deps import get_delete_user_usecase, get_bearer_token
from .. import router

from ...schemas import TokenVerifyErrorResponse, UserNotExistsResponse

@router.delete(
    path="",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Пользователь успешно удалён, токен отозван"},
        401: {
            "description": "Токен отсутствует / невалиден / истёк",
            "content": {
                "application/json": {
                    "schema": TokenVerifyErrorResponse.model_json_schema(),
                },
            },
        },
        404: {
            "description": "Пользователь не существует",
            "content": {
                "application/json": {
                    "schema": UserNotExistsResponse.model_json_schema(),
                }
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
    except UserNotExists as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.args[0]
        ) from e
    except TokenVerifyError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=e.args[0]
        ) from e
