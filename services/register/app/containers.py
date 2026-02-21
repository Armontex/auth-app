from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import async_sessionmaker

from services.auth.app.ports import IPasswordHasher

from ..app.usecases import RegisterUseCase
from .uow import RegisterUoW


class RegisterContainer(containers.DeclarativeContainer):
    password_hasher = providers.Dependency(IPasswordHasher)
    session_maker = providers.Dependency(async_sessionmaker)

    register_uow = providers.Factory(RegisterUoW, session_maker=session_maker)

    # ==== UseCases ====

    register_usecase = providers.Factory(
        RegisterUseCase, uow=register_uow, password_hasher=password_hasher
    )
