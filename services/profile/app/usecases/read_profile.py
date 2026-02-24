from common.ports import IProfile
from ..uow import ProfileUoW
from ..exc import ProfileNotFound


class ReadProfileUseCase:

    def __init__(self, uow: ProfileUoW) -> None:
        self._uow = uow

    async def execute(self, user_id: int) -> IProfile:
        """
        Raises:
            ProfileNotFound: Профиль не найден.
        """
        async with self._uow as repos:
            prof = await repos.profile.get_by_user_id(user_id)
            if not prof:
                raise ProfileNotFound
            return prof
