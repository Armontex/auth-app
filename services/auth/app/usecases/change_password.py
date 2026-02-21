from ..ports import IUoW, IUserRepository, IPasswordHasher
from .login import LoginUseCase

from ...domain.models import ChangePasswordForm


class ChangePasswordUseCase:

    def __init__(
        self,
        uow: IUoW[IUserRepository],
        password_hasher: IPasswordHasher,
        login_usecase: LoginUseCase,
    ) -> None:
        self._uow = uow
        self._hasher = password_hasher
        self._login_usecase = login_usecase

    async def execute(self, form: ChangePasswordForm) -> None:
        user = await self._login_usecase.authenticate(form)

        async with self._uow as repo:
            new_password_hash = self._hasher.hash(form.new_password.value)
            await repo.set_password_hash(user, new_password_hash)
