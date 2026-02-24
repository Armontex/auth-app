from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import async_sessionmaker

from .uow import UserUoW, SetRoleUoW, InitRbacUoW
from .usecases import (
    SetRoleUseCase,
    InitRbacUseCase,
    ReadMeRolesUseCase,
    ReadRolesUseCase,
    ReadMePermissionsUseCase,
    ReadPermissionsUseCase,
)


class RbacContainer(containers.DeclarativeContainer):
    session_maker = providers.Dependency(async_sessionmaker)

    init_rbac_uow = providers.Factory(InitRbacUoW, session_maker=session_maker)
    set_role_uow = providers.Factory(SetRoleUoW, session_maker=session_maker)
    user_uow = providers.Factory(UserUoW, session_maker=session_maker)

    # ==== UseCases ====

    init_rbac_usecase = providers.Factory(InitRbacUseCase, uow=init_rbac_uow)
    set_role_usecase = providers.Factory(SetRoleUseCase, uow=set_role_uow)
    read_roles_usecase = providers.Factory(ReadRolesUseCase, uow=user_uow)
    read_perms_usecase = providers.Factory(ReadPermissionsUseCase, uow=user_uow)
    read_me_roles_usecase = providers.Factory(
        ReadMeRolesUseCase, read_roles=read_roles_usecase
    )
    read_me_perms_usecase = providers.Factory(
        ReadMePermissionsUseCase, read_perms=read_perms_usecase
    )

    set_role_func = providers.Object(SetRoleUseCase.set_role)
