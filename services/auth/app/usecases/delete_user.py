from ..ports import IUoW, IUserRepository
from .logout import LogoutUseCase
from .authorize import AuthorizeUseCase


class DeleteUserUseCase:

    def __init__(
        self,
        uow: IUoW[IUserRepository],
        logout_usecase: LogoutUseCase,
        authorize_usecase: AuthorizeUseCase,
    ) -> None:
        self._uow = uow
        self._logout = logout_usecase
        self._authorize = authorize_usecase

    async def execute(self, token: str) -> None:
        """
        Raises:
            TokenVerifyError: Неверный, истёкший или отозванный токен.
            UserNotExists: Пользователь не существует.
        """
        user_id = await self._authorize.verify_token(token)

        async with self._uow as repo:
            await repo.delete_user(user_id)

        await self._logout.execute(token)
