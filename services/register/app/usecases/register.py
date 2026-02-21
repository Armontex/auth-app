from services.auth.app.usecases import (
    RegisterUseCase as AuthRegisterUseCase,
    RegisterForm as AuthRegisterForm,
)
from services.auth.app.ports import IUser, IUserRepository, IPasswordHasher

from services.profile.app.usecases import (
    RegisterUseCase as ProfileRegisterUseCase,
    RegisterForm as ProfileRegisterForm,
)
from services.profile.app.ports import IProfileRepository

from ..ports import IUoW


class RegisterUseCase:

    def __init__(
        self,
        uow: IUoW[tuple[IUserRepository, IProfileRepository]],
        password_hasher: IPasswordHasher,
    ) -> None:
        self._uow = uow
        self._hasher = password_hasher

    async def execute(
        self, auth_form: AuthRegisterForm, profile_form: ProfileRegisterForm
    ) -> IUser:
        """
        Raises:
            EmailAlreadyExists: Пользователь с таким `email` уже существует.
            ProfileAlreadyExists: Профиль с таким `user_id` уже существует.
        """
        async with self._uow as (auth_repo, profile_repo):
            auth_usecase = AuthRegisterUseCase(auth_repo, self._hasher)
            profile_usecase = ProfileRegisterUseCase(profile_repo)

            user = await auth_usecase.execute(auth_form)
            await profile_usecase.execute(user.id, profile_form)
            return user
