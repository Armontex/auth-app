from ...deps import get_profile_container
from services.profile.app.usecases import UpdateUseCase
from services.profile.app.containers import ProfileContainer
from fastapi import Depends


def get_update_usecase(
    container: ProfileContainer = Depends(get_profile_container),
) -> UpdateUseCase:
    return container.update_usecase()
