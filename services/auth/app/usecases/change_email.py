from .login import LoginUseCase
from ..uow import UserUoW
from ...domain.models import ChangeEmailForm


class ChangeEmailUseCase:

    def __init__(
        self,
        uow: UserUoW,
        login_usecase: LoginUseCase,
    ) -> None:
        self._uow = uow
        self._login_usecase = login_usecase

    async def execute(self, form: ChangeEmailForm) -> None:
        """
        Raises:
            LoginError: Неверные учетные данные.
            EmailAlreadyExists: Пользователь с таким `email` уже существует.
        """
        user = await self._login_usecase.authenticate(form)
        async with self._uow as repos:
            await repos.user.set_email(user, form.new_email.value)
