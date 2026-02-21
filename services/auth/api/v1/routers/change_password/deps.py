from fastapi import Depends

from services.auth.app.containers import AuthContainer
from services.auth.app.usecases import ChangePasswordUseCase

from ...deps import validate_content_type, get_auth_container


def get_change_password_usecase(
    container: AuthContainer = Depends(get_auth_container),
) -> ChangePasswordUseCase:
    return container.change_password_usecase()
