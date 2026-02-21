from fastapi import Depends
from services.auth.app.containers import AuthContainer
from services.auth.app.usecases import LogoutUseCase
from ...deps import get_bearer_token, get_auth_container


def get_logout_usecase(
    container: AuthContainer = Depends(get_auth_container),
) -> LogoutUseCase:
    return container.logout_usecase()
