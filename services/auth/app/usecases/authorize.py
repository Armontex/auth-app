from ..ports import IJWTManager, IUser
from ..exc import UserNotExists
from ..uow import UserUoW


class AuthorizeUseCase:

    def __init__(self, uow: UserUoW, jwt_manager: IJWTManager) -> None:
        self._uow = uow
        self._jwt = jwt_manager

    async def verify_token(self, token: str) -> int:
        """
        Raises:
            TokenVerifyError: Неверный, истёкший или отозванный токен.
        """
        return await self._jwt.verify(token)

    async def execute(self, token: str) -> IUser:
        """
        Raises:
            TokenVerifyError: Неверный, истёкший или отозванный токен.
        """
        user_id = await self.verify_token(token)
        async with self._uow as repos:
            user = await repos.user.get_active_user_by_id(user_id)
            if not user:
                raise UserNotExists
            return user
