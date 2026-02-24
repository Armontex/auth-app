from fastapi import Depends
from api.v1.deps import RequirePermission
from common.ports import IUser
from services.rbac.domain.const import Permission
from services.profile.app.usecases import UpdateUseCase
from services.profile.app.containers import ProfileContainer
from ...deps import get_profile_container


def get_update_usecase(
    container: ProfileContainer = Depends(get_profile_container),
) -> UpdateUseCase:
    return container.update_usecase()


def require_profile_me_update(
    user: IUser = Depends(RequirePermission(Permission.PROFILE_ME_UPDATE)),
) -> IUser:
    return user
