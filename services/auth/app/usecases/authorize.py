from ..ports import IJWTManager, IUser, IUoW, IUserRepository
from ..exc import UserNotExists


class AuthorizeUseCase:

    def __init__(self, uow: IUoW[IUserRepository], jwt_manager: IJWTManager) -> None:
        self._uow = uow
        self._jwt = jwt_manager

    async def execute(self, token: str) -> IUser:
        """
        Raises:
            TokenVerifyError: Неверный, истёкший или отозванный токен.
        """
        user_id = await self._jwt.verify(token)
        async with self._uow as repo:
            user = await repo.get_active_user_by_id(user_id)
            if not user:
                raise UserNotExists
            return user
