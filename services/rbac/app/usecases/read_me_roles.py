from common.ports import IUser, IRole
from .read_roles import ReadRolesUseCase


class ReadMeRolesUseCase:

    def __init__(self, read_roles: ReadRolesUseCase) -> None:
        self._read_roles = read_roles

    async def execute(self, user: IUser) -> list[IRole]:
        """
        Raises:
            UserNotExists: Такого пользователя не существует.
        """
        return await self._read_roles.execute(user.id)
