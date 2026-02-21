from ..ports import IUoW, IProfileRepository, IJWTManager, IProfile
from ...domain.models import UpdateForm
from ..exc import ProfileNotFound


class UpdateUseCase:
    def __init__(self, uow: IUoW[IProfileRepository], jwt_manager: IJWTManager) -> None:
        self._uow = uow
        self._jwt_manager = jwt_manager

    async def execute(self, token: str, form: UpdateForm) -> None:
        """
        Raises:
            ProfileNotFound: Если профиль пользователя не найден.
            TokenVerifyError: Если токен недействителен.
        """
        async with self._uow as repo:
            user_id = await self._jwt_manager.verify(token)
            profile = await repo.get_by_user_id(user_id)

            if not profile:
                raise ProfileNotFound()

            if form.first_name is not None:
                await repo.set_first_name(profile, form.first_name.value)
            if form.last_name is not None:
                await repo.set_last_name(profile, form.last_name.value)
            if form.middle_name is not None:
                await repo.set_middle_name(profile, form.middle_name.value)
