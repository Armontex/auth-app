from common.exc import RepositoryError
from ..ports import IUsersRepository, IUser, IPasswordHasher
from ..exc import UseCaseError
from ...domain.models import RegisterForm


class RegisterError(UseCaseError): ...


class RegisterUseCase:

    def __init__(
        self, user_repo: IUsersRepository, password_hasher: IPasswordHasher
    ) -> None:
        self._user_repo = user_repo
        self._hasher = password_hasher

    async def execute(self, form: RegisterForm) -> IUser:
        try:
            return await self._user_repo.add_user(
                first_name=form.first_name,
                middle_name=form.middle_name,
                last_name=form.last_name,
                email=form.email.value,
                password_hash=self._hasher.hash(form.password),
            )
        except RepositoryError as e:
            raise RegisterError("User with this email already exists.") from e
