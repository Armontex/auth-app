from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import async_sessionmaker

from .uow import SetRoleUoW, InitRbacUoW
from .usecases import SetRoleUseCase, InitRbacUseCase


class RbacContainer(containers.DeclarativeContainer):
    session_maker = providers.Dependency(instance_of=async_sessionmaker)

    set_role_uow = providers.Factory(SetRoleUoW, session_maker=session_maker)
    init_rbac_uow = providers.Factory(InitRbacUoW, session_maker=session_maker)

    # ==== UseCases ====

    set_role_usecase = providers.Factory(SetRoleUseCase, uow=set_role_uow)
    init_rbac_usecase = providers.Factory(InitRbacUseCase, uow=init_rbac_uow)
