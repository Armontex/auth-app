from ..ports import IUoW, IUserRepository
from .login import LoginUseCase
from ..exc import EmailAlreadyExists, ChangeEmailError

from ...domain.models import ChangeEmailForm


class ChangeEmailUseCase:

    def __init__(
        self,
        uow: IUoW[IUserRepository],
        login_usecase: LoginUseCase,
    ) -> None:
        self._uow = uow
        self._login_usecase = login_usecase

    async def execute(self, form: ChangeEmailForm) -> None:
        user = await self._login_usecase.authenticate(form)

        try:
            async with self._uow as repo:
                await repo.set_email(user, form.new_email.value)
        except EmailAlreadyExists as e:
            raise ChangeEmailError(str(e)) from e
