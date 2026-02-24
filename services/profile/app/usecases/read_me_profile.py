from common.ports import IUser, IProfile
from .read_profile import ReadProfileUseCase


class ReadMeProfileUseCase:

    def __init__(self, read_profile: ReadProfileUseCase) -> None:
        self._read_prof = read_profile

    async def execute(self, user: IUser) -> IProfile:
        """
        Raises:
            ProfileNotFound: Профиль не найден.
        """
        return await self._read_prof.execute(user.id)
