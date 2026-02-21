from fastapi import Depends

from services.auth.app.containers import AuthContainer
from services.auth.app.usecases import ChangeEmailUseCase

from ...deps import validate_content_type, get_auth_container


def get_change_email_usecase(
    container: AuthContainer = Depends(get_auth_container),
) -> ChangeEmailUseCase:
    return container.change_email_usecase()
