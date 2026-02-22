from .login import LoginUseCase
from ..uow import UserUoW
from ..ports import IPasswordHasher
from ...domain.models import ChangePasswordForm


class ChangePasswordUseCase:

    def __init__(
        self,
        uow: UserUoW,
        password_hasher: IPasswordHasher,
        login_usecase: LoginUseCase,
    ) -> None:
        self._uow = uow
        self._hasher = password_hasher
        self._login_usecase = login_usecase

    async def execute(self, form: ChangePasswordForm) -> None:
        """
        Raises:
            LoginError: Неверные учетные данные.
        """
        user = await self._login_usecase.authenticate(form)

        async with self._uow as repos:
            new_password_hash = self._hasher.hash(form.new_password.value)
            await repos.user.set_password_hash(user, new_password_hash)
