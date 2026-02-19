from ..ports import IUserRepository, IPasswordHasher, IJWTManager
from .exc import AppError
from ...domain.models import LoginForm


class LoginError(AppError): ...


class LoginUseCase:

    def __init__(
        self,
        user_repo: IUserRepository,
        password_hasher: IPasswordHasher,
        jwt_manager: IJWTManager,
    ) -> None:
        self._user_repo = user_repo
        self._hasher = password_hasher
        self._jwt = jwt_manager

    async def execute(self, form: LoginForm) -> str:
        check_user = await self._user_repo.get_user_by_email(form.email.value)
        if (
            not check_user
            or not check_user.is_active
            or not self._hasher.verify(form.password, check_user.password_hash)
        ):
            raise LoginError("Invalid login or password")

        return self._jwt.issue_access(check_user.id)
