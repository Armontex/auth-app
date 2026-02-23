from common.ports import IProfile
from .read_me_profile import ReadMeProfileUseCase
from ..uow import ProfileUoW
from ..exc import ProfileNotFound


class ReadProfileUseCase:

    def __init__(self, uow: ProfileUoW, read_me_prof: ReadMeProfileUseCase) -> None:
        self._uow = uow
        self._read_me_prof = read_me_prof

    async def execute(self, user_id: int) -> IProfile:
        """
        Raises:
            ProfileNotFound: Профиль не найден.
        """
        async with self._uow as repos:
            prof = await repos.profile.get_by_user_id(user_id)
            if not prof:
                raise ProfileNotFound
            return self._read_me_prof.execute(prof.user)
