from common.ports import IPermission

from services.auth.app.exc import UserNotExists

from ..uow import UserUoW


class ReadPermissionsUseCase:

    def __init__(self, uow: UserUoW) -> None:
        self._uow = uow

    async def execute(self, user_id: int) -> set[IPermission]:
        """
        Raises:
            UserNotExists: Такого пользователя не существует.
        """
        async with self._uow as repos:
            user = await repos.user.get_active_user_by_id(user_id)
            if not user:
                raise UserNotExists

            return {perm for role in user.roles for perm in role.permissions}
