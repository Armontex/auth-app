from common.ports import IRole

from services.auth.app.exc import UserNotExists

from .read_me_roles import ReadMeRolesUseCase
from ..uow import UserUoW


class ReadRolesUseCase:

    def __init__(self, uow: UserUoW, read_me_roles: ReadMeRolesUseCase) -> None:
        self._uow = uow
        self._read_me_roles = read_me_roles

    async def execute(self, user_id: int) -> list[IRole]:
        """
        Raises:
            UserNotExists: Такого пользователя не существует.
        """
        async with self._uow as repos:
            user = await repos.user.get_active_user_by_id(user_id)
            if not user:
                raise UserNotExists
            return self._read_me_roles.execute(user)
