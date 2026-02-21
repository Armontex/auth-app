from ...deps import get_auth_container
from services.auth.app.containers import AuthContainer
from services.auth.app.usecases import RegisterUseCase
from fastapi import Depends


def get_register_usecase(
    container: AuthContainer = Depends(get_auth_container),
) -> RegisterUseCase:
    return container.register_usecase()
