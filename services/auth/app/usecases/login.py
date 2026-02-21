from ..ports import IUoW, IUserRepository, IPasswordHasher, IJWTManager, IUser
from ..exc import LoginError
from ...domain.models import LoginForm


class LoginUseCase:

    def __init__(
        self,
        uow: IUoW[IUserRepository],
        password_hasher: IPasswordHasher,
        jwt_manager: IJWTManager,
    ) -> None:
        self._uow = uow
        self._hasher = password_hasher
        self._jwt = jwt_manager

    async def authenticate(self, form: LoginForm) -> IUser:
        async with self._uow as repo:
            user = await repo.get_user_by_email(form.email.value)
            if (
                not user
                or not user.is_active
                or not self._hasher.verify(form.password, user.password_hash)
            ):
                raise LoginError()
            return user

    async def execute(self, form: LoginForm) -> str:
        user = await self.authenticate(form)
        return self._jwt.issue_access(user.id)
    
