from ..ports import IUsersRepository, IUser, IPasswordHasher
from ...domain.models.register import RegisterForm
from ..exc import UseCaseError


class RegisterError(UseCaseError): ...


class RegisterUseCase:

    def __init__(
        self, user_repo: IUsersRepository, password_hasher: IPasswordHasher
    ) -> None:
        self._user_repo = user_repo
        self._hasher = password_hasher

    async def execute(self, form: RegisterForm) -> IUser:
        check_user = await self._user_repo.get_user_by_email(email=form.email.value)
        if check_user:
            raise RegisterError("User with this email already exists.")

        return await self._user_repo.add_user(
            first_name=form.first_name,
            middle_name=form.middle_name,
            last_name=form.last_name,
            email=form.email.value,
            password_hash=self._hasher.hash(form.password),
        )
