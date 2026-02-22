from services.auth.app.usecases import (
    RegisterUseCase as AuthRegisterUseCase,
    RegisterForm as AuthRegisterForm,
)
from services.auth.app.ports import IUserRepository
from common.ports import IUser, IPasswordHasher

from services.profile.app.usecases import (
    RegisterUseCase as ProfileRegisterUseCase,
    RegisterForm as ProfileRegisterForm,
)
from services.profile.app.ports import IProfileRepository

from services.rbac.app.usecases import SetRoleUseCase
from services.rbac.app.ports import IUserRolesRepository, IRoleRepository
from services.rbac.domain.const import Role

from ..ports import IUoW


class RegisterUseCase:

    def __init__(
        self,
        uow: IUoW[
            tuple[
                IUserRepository,
                IProfileRepository,
                IRoleRepository,
                IUserRolesRepository,
            ]
        ],
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
            RoleNotFound: Роль не найдена.
        """
        async with self._uow as (auth_repo, profile_repo, role_repo, user_roles_repo):
            auth_reg_usecase = AuthRegisterUseCase(auth_repo, self._hasher)
            profile_reg_usecase = ProfileRegisterUseCase(profile_repo)

            user = await auth_reg_usecase.execute(auth_form)
            await profile_reg_usecase.execute(user.id, profile_form)

            await SetRoleUseCase.set_role(
                user.id, Role.USER, role_repo, user_roles_repo
            )

            return user
