from ..ports import IJWTManager, IUoW, IUserRepository


class DeleteUserUseCase:

    def __init__(
        self,
        uow: IUoW[IUserRepository],
        jwt_manager: IJWTManager,
    ) -> None:
        self._uow = uow
        self._jwt = jwt_manager

    async def execute(self, token: str) -> None:
        """
        Raises:
            TokenVerifyError: Неверный, истёкший или отозванный токен.
            UserNotExists: Пользователь не существует.
        """
        user_id = await self._jwt.verify(token)
        await self._jwt.revoke(token)

        async with self._uow as repo:
            await repo.delete_user(user_id)
