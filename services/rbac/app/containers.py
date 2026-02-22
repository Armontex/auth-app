from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import async_sessionmaker

from .uow import UserUoW, SetRoleUoW, InitRbacUoW
from .usecases import (
    SetRoleUseCase,
    InitRbacUseCase,
    ReadMeRolesUseCase,
    ReadRolesUseCase,
)


class RbacContainer(containers.DeclarativeContainer):
    session_maker = providers.Dependency(async_sessionmaker)

    init_rbac_uow = providers.Factory(InitRbacUoW, session_maker=session_maker)
    set_role_uow = providers.Factory(SetRoleUoW, session_maker=session_maker)
    user_uow = providers.Factory(UserUoW, session_maker=session_maker)

    # ==== UseCases ====

    init_rbac_usecase = providers.Factory(InitRbacUseCase, uow=init_rbac_uow)
    set_role_usecase = providers.Factory(SetRoleUseCase, uow=set_role_uow)
    read_me_roles_usecase = providers.Factory(ReadMeRolesUseCase)
    read_roles_usecase = providers.Factory(
        ReadRolesUseCase, uow=user_uow, read_me_roles=read_me_roles_usecase
    )
    set_role_func = SetRoleUseCase.set_role
