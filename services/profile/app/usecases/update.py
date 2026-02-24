from common.ports import IUser, IProfile

from ..uow import ProfileUoW
from ...domain.models import UpdateForm


class UpdateUseCase:
    def __init__(self, uow: ProfileUoW) -> None:
        self._uow = uow

    async def execute(self, user: IUser, form: UpdateForm) -> IProfile:

        async with self._uow as repos:
            profile = await repos.profile.get_by_user_id(user.id)
            
            if not profile:
                raise

            if form.first_name is not None:
                await repos.profile.set_first_name(profile, form.first_name.value)
            if form.last_name is not None:
                await repos.profile.set_last_name(profile, form.last_name.value)
            if form.middle_name is not None:
                await repos.profile.set_middle_name(profile, form.middle_name.value)

            return profile
