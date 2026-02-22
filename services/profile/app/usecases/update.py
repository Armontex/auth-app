from ..ports import IUoW, IProfileRepository
from ...domain.models import UpdateForm

from common.ports import IUser, IProfile


class UpdateUseCase:
    def __init__(self, uow: IUoW[IProfileRepository]) -> None:
        self._uow = uow

    async def execute(self, user: IUser, form: UpdateForm) -> IProfile:
        profile = user.profile

        async with self._uow as repo:

            if form.first_name is not None:
                await repo.set_first_name(profile, form.first_name.value)
            if form.last_name is not None:
                await repo.set_last_name(profile, form.last_name.value)
            if form.middle_name is not None:
                await repo.set_middle_name(profile, form.middle_name.value)

            await repo.refresh(profile)
            return profile
