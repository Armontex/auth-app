from common.ports import IUser, IPermission
from .read_perms import ReadPermissionsUseCase


class ReadMePermissionsUseCase:

    def __init__(self, read_perms: ReadPermissionsUseCase) -> None:
        self._read_perms = read_perms

    async def execute(self, user: IUser) -> set[IPermission]:
        """
        Raises:
            UserNotExists: Такого пользователя не существует.
        """
        return await self._read_perms.execute(user.id)
