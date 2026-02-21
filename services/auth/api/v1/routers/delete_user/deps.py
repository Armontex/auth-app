from fastapi import Depends

from services.auth.app.containers import AuthContainer
from services.auth.app.usecases import DeleteUserUseCase

from ...deps import get_bearer_token, get_auth_container


def get_delete_user_usecase(
    container: AuthContainer = Depends(get_auth_container),
) -> DeleteUserUseCase:
    return container.delete_user_usecase()
