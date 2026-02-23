from fastapi import Depends

from api.v1.deps import RequirePermission
from common.ports import IUser

from services.profile.app.usecases import ReadMeProfileUseCase, ReadProfileUseCase
from services.profile.app.containers import ProfileContainer
from services.rbac.domain.const import Permission

from ...deps import get_profile_container


def get_read_me_prof_usecase(
    container: ProfileContainer = Depends(get_profile_container),
) -> ReadMeProfileUseCase:
    return container.read_me_prof_usecase()


def get_read_prof_usecase(
    container: ProfileContainer = Depends(get_profile_container),
) -> ReadProfileUseCase:
    return container.read_prof_usecase()


async def require_profile_me_read() -> IUser:
    return await RequirePermission(Permission.PROFILE_ME_READ)()


async def require_profile_read() -> IUser:
    return await RequirePermission(Permission.PROFILE_READ)()
