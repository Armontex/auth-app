from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import async_sessionmaker

from .usecases import UpdateUseCase
from .uow import UpdateUoW
from .ports import IJWTManager


class ProfileContainer(containers.DeclarativeContainer):
    session_maker = providers.Dependency(instance_of=async_sessionmaker)
    jwt_manager = providers.Dependency(instance_of=IJWTManager)

    update_uow = providers.Factory(UpdateUoW, session_maker=session_maker)

    # ==== UseCases ====

    update_usecase = providers.Factory(
        UpdateUseCase, uow=update_uow, jwt_manager=jwt_manager
    )
