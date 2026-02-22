from ..ports import IUserRepository, IUser, IPasswordHasher
from ...domain.models import RegisterForm


class RegisterUseCase:

    def __init__(self, repo: IUserRepository, password_hasher: IPasswordHasher) -> None:
        self._repo = repo
        self._hasher = password_hasher

    async def execute(self, form: RegisterForm) -> IUser:
        """
        Raises:
            EmailAlreadyExists: Пользователь с таким `email` уже существует.
        """
        return await self._repo.add(
            email=form.email.value,
            password_hash=self._hasher.hash(form.password.value),
        )
