from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import async_sessionmaker

from config.settings import settings

from .ports import IProfileUoW
from .uow.profile import ProfileUoW


class ProfileContainer(containers.DeclarativeContainer):
    session_maker = providers.Dependency(instance_of=async_sessionmaker)

    # wiring_config = containers.WiringConfiguration(
    #     modules=["services.profile.api.v1.routers"]
    # )

    # ==== Infra ====

    profile_uow = providers.Factory[IProfileUoW](
        ProfileUoW, session_factory=session_maker
    )

    # ==== UseCases ====
