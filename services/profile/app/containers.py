from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import async_sessionmaker

from .usecases import (
    UpdateUseCase,
    RegisterUseCase,
    ReadMeProfileUseCase,
    ReadProfileUseCase,
)
from .uow import ProfileUoW


class ProfileContainer(containers.DeclarativeContainer):
    session_maker = providers.Dependency(async_sessionmaker)

    profile_uow = providers.Factory(ProfileUoW, session_maker=session_maker)

    # ==== UseCases ====

    update_usecase = providers.Factory(UpdateUseCase, uow=profile_uow)
    read_me_prof_usecase = providers.Factory(ReadMeProfileUseCase)
    read_prof_usecase = providers.Factory(
        ReadProfileUseCase, uow=profile_uow, read_me_prof=read_me_prof_usecase
    )

    # ==== Factory ====

    register_factory = providers.Factory(RegisterUseCase).provider
