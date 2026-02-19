from ..ports import IUserUoW, IPasswordHasher, IJWTManager
from .exc import AppError
from ...domain.models import LoginForm


class LoginError(AppError): ...


class LoginUseCase:

    def __init__(
        self,
        uow: IUserUoW,
        password_hasher: IPasswordHasher,
        jwt_manager: IJWTManager,
    ) -> None:
        self._uow = uow
        self._hasher = password_hasher
        self._jwt = jwt_manager

    async def execute(self, form: LoginForm) -> str:
        async with self._uow as repo:
            check_user = await repo.get_user_by_email(form.email.value)
            if (
                not check_user
                or not check_user.is_active
                or not self._hasher.verify(form.password, check_user.password_hash)
            ):
                raise LoginError("Invalid login or password")

            return self._jwt.issue_access(check_user.id)
