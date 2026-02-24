from common.ports import IRole

from services.auth.app.exc import UserNotExists

from ..uow import UserUoW


class ReadRolesUseCase:

    def __init__(self, uow: UserUoW) -> None:
        self._uow = uow

    async def execute(self, user_id: int) -> list[IRole]:
        """
        Raises:
            UserNotExists: Такого пользователя не существует.
        """
        async with self._uow as repos:
            user = await repos.user.get_active_user_by_id(user_id)
            if not user:
                raise UserNotExists
            return user.roles
