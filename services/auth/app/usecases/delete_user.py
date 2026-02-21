from ..ports import IJWTManager, IUoW, IUserRepository
from ..exc import DeleteUserError, TokenVerifyError, UserNotExists





class DeleteUserUseCase:

    def __init__(
        self,
        uow: IUoW[IUserRepository],
        jwt_manager: IJWTManager,
    ) -> None:
        self._uow = uow
        self._jwt = jwt_manager

    async def execute(self, token: str) -> None:
        try:
            user_id = await self._jwt.verify(token)
            await self._jwt.revoke(token)

            async with self._uow as repo:
                await repo.delete_user(user_id)

        except (TokenVerifyError, UserNotExists) as e:
            raise DeleteUserError(str(e)) from e
