from common.ports import IPermission

from services.auth.app.exc import UserNotExists

from .read_me_perms import ReadMePermissionsUseCase
from ..uow import UserUoW


class ReadPermissionsUseCase:

    def __init__(self, uow: UserUoW, read_me_perms: ReadMePermissionsUseCase) -> None:
        self._uow = uow
        self._read_me_perms = read_me_perms

    async def execute(self, user_id: int) -> set[IPermission]:
        """
        Raises:
            UserNotExists: Такого пользователя не существует.
        """
        async with self._uow as repos:
            user = await repos.user.get_active_user_by_id(user_id)
            if not user:
                raise UserNotExists

            return self._read_me_perms.execute(user)
