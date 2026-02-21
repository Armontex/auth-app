from fastapi import Depends

from services.auth.app.containers import AuthContainer
from services.auth.app.usecases import LoginUseCase

from ...deps import validate_content_type, get_auth_container


def get_login_usecase(
    container: AuthContainer = Depends(get_auth_container),
) -> LoginUseCase:
    return container.login_usecase()
