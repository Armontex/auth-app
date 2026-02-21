from ..ports import IUoW, IUserRepository, IUser, IPasswordHasher
from ..exc import EmailAlreadyExists, RegisterError
from ...domain.models import RegisterForm


class RegisterUseCase:

    def __init__(
        self, uow: IUoW[IUserRepository], password_hasher: IPasswordHasher
    ) -> None:
        self._uow = uow
        self._hasher = password_hasher

    async def execute(self, form: RegisterForm) -> IUser:
        try:
            async with self._uow as repo:
                return await repo.add(
                    email=form.email.value,
                    password_hash=self._hasher.hash(form.password.value),
                )
        except EmailAlreadyExists as e:
            raise RegisterError(str(e)) from e
