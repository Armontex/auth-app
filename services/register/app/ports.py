from typing import Protocol, runtime_checkable

from common.ports import IPasswordHasher

from services.auth.app.usecases import RegisterUseCase as AuthRegister
from services.auth.app.ports import IUserRepository

from services.profile.app.usecases import RegisterUseCase as ProfileRegister
from services.profile.app.ports import IProfileRepository

from services.rbac.domain.const import Role
from services.rbac.app.ports import IRoleRepository, IUserRolesRepository


@runtime_checkable
class AuthResisterFactory(Protocol):
    def __call__(
        self, repo: IUserRepository, hasher: IPasswordHasher
    ) -> AuthRegister: ...


@runtime_checkable
class ProfileRegisterFactory(Protocol):
    def __call__(self, repo: IProfileRepository) -> ProfileRegister: ...


@runtime_checkable
class SetRoleFunc(Protocol):
    async def __call__(
        self,
        user_id: int,
        role: Role,
        role_repo: IRoleRepository,
        user_roles_repo: IUserRolesRepository,
    ) -> None: ...
