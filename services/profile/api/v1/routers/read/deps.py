from ...deps import get_profile_container
from services.profile.app.usecases import ReadMeProfileUseCase, ReadProfileUseCase
from services.profile.app.containers import ProfileContainer
from fastapi import Depends


def get_read_me_prof_usecase(
    container: ProfileContainer = Depends(get_profile_container),
) -> ReadMeProfileUseCase:
    return container.read_me_prof_usecase()


def get_read_prof_usecase(
    container: ProfileContainer = Depends(get_profile_container),
) -> ReadProfileUseCase:
    return container.read_prof_usecase()
