from common.ports import IUser, IPasswordHasher

from ..uow import RegisterUoW
from ..ports import AuthResisterFactory, ProfileRegisterFactory, SetRoleFunc

from services.auth.app.usecases import RegisterForm as AuthRegisterForm
from services.profile.app.usecases import RegisterForm as ProfileRegisterForm
from services.rbac.domain.const import Role


class RegisterUseCase:

    def __init__(
        self,
        uow: RegisterUoW,
        password_hasher: IPasswordHasher,
        make_auth_register: AuthResisterFactory,
        make_profile_register: ProfileRegisterFactory,
        set_role: SetRoleFunc,
    ) -> None:
        self._uow = uow
        self._hasher = password_hasher
        self._make_auth_register = make_auth_register
        self._make_profile_register = make_profile_register
        self._set_role = set_role

    async def _reg_user(
        self, auth_form: AuthRegisterForm, profile_form: ProfileRegisterForm, role: Role
    ) -> IUser:
        """
        Raises:
            EmailAlreadyExists: Пользователь с таким `email` уже существует.
            ProfileAlreadyExists: Профиль с таким `user_id` уже существует.
            RoleNotFound: Роль не найдена.
        """
        async with self._uow as repos:
            auth_register = self._make_auth_register(repos.user, self._hasher)
            prof_register = self._make_profile_register(repos.profile)

            user = await auth_register.execute(auth_form)
            await prof_register.execute(user.id, profile_form)

            await self._set_role(user.id, role, repos.role, repos.user_roles)
            return user

    async def execute(
        self, auth_form: AuthRegisterForm, profile_form: ProfileRegisterForm
    ) -> IUser:
        """
        Raises:
            EmailAlreadyExists: Пользователь с таким `email` уже существует.
            ProfileAlreadyExists: Профиль с таким `user_id` уже существует.
            RoleNotFound: Роль не найдена.
        """
        return await self._reg_user(auth_form, profile_form, Role.USER)

    async def mock_execute(self) -> None:
        from services.register.api.v1.routers.register.mappers import (
            map_request_to_auth_form,
            map_request_to_profile_form,
        )
        from services.register.api.v1.routers.register.schemas import RegisterRequests

        # ==== LimitedUser ====
        limited_user_request = RegisterRequests(
            email="limited@example.com",
            first_name="SomeName",
            last_name="SomeLastName",
            password="qwerty123",
            confirm_password="qwerty123",
        )
        limited_user_auth_form = map_request_to_auth_form(limited_user_request)
        limited_user_prof_form = map_request_to_profile_form(limited_user_request)

        await self._reg_user(
            limited_user_auth_form, limited_user_prof_form, Role.LIMITED_USER
        )

        # ==== User ====
        user_request = RegisterRequests(
            email="user@example.com",
            first_name="SomeName",
            last_name="SomeLastName",
            password="qwerty123",
            confirm_password="qwerty123",
        )

        user_auth_form = map_request_to_auth_form(user_request)
        user_prof_form = map_request_to_profile_form(user_request)

        await self._reg_user(user_auth_form, user_prof_form, Role.USER)

        # ==== Admin ====

        admin_request = RegisterRequests(
            email="admin@example.com",
            first_name="SomeName",
            last_name="SomeLastName",
            password="qwerty123",
            confirm_password="qwerty123",
        )

        admin_auth_form = map_request_to_auth_form(admin_request)
        admin_prof_form = map_request_to_profile_form(admin_request)

        await self._reg_user(admin_auth_form, admin_prof_form, Role.ADMIN)
