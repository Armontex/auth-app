from fastapi import Depends
from ...deps import validate_content_type, get_register_container
from services.register.app.containers import RegisterContainer
from services.register.app.usecases import RegisterUseCase


def get_register_usecase(
    container: RegisterContainer = Depends(get_register_container),
) -> RegisterUseCase:
    return container.register_usecase()

