from common.exc import RepositoryError
from ..ports import IUserUoW, IUser, IPasswordHasher
from .exc import AppError
from ...domain.models import RegisterForm


class RegisterError(AppError): ...


class RegisterUseCase:

    def __init__(self, uow: IUserUoW, password_hasher: IPasswordHasher) -> None:
        self._uow = uow
        self._hasher = password_hasher

    async def execute(self, form: RegisterForm) -> IUser:
        try:
            async with self._uow as repo:
                return await repo.add_user(
                    first_name=form.first_name,
                    middle_name=form.middle_name,
                    last_name=form.last_name,
                    email=form.email.value,
                    password_hash=self._hasher.hash(form.password),
                )
        except RepositoryError as e:
            raise RegisterError("User with this email already exists.") from e
