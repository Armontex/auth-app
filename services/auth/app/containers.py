from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import async_sessionmaker

from config.settings import settings

from .uow import UserUoW
from .usecases import (
    LoginUseCase,
    LogoutUseCase,
    DeleteUserUseCase,
    ChangePasswordUseCase,
    ChangeEmailUseCase,
    AuthorizeUseCase,
    RegisterUseCase,
)

from ..infra.db.tokens.repos import TokenRepositoryRedis
from ..infra.jwt.adapters.app_adapter import JWTManagerAdapter
from ..infra.security.hasher import PasswordHasher


class AuthContainer(containers.DeclarativeContainer):
    session_maker = providers.Dependency(async_sessionmaker)

    # ==== Infra ====

    redis_token_repo = providers.Singleton(TokenRepositoryRedis, url=settings.redis_url)

    jwt_manager = providers.Singleton(
        JWTManagerAdapter,
        token_repo=redis_token_repo,
        secret_key=settings.secret_key.get_secret_value(),
    )

    password_hasher = providers.Singleton(PasswordHasher)

    user_uow = providers.Factory(UserUoW, session_maker=session_maker)

    # ==== UseCases ====

    login_usecase = providers.Factory(
        LoginUseCase,
        uow=user_uow,
        password_hasher=password_hasher,
        jwt_manager=jwt_manager,
    )

    logout_usecase = providers.Factory(
        LogoutUseCase,
        jwt_manager=jwt_manager,
    )

    change_password_usecase = providers.Factory(
        ChangePasswordUseCase,
        uow=user_uow,
        password_hasher=password_hasher,
        login_usecase=login_usecase,
    )

    change_email_usecase = providers.Factory(
        ChangeEmailUseCase, uow=user_uow, login_usecase=login_usecase
    )

    authorize_usecase = providers.Factory(
        AuthorizeUseCase, uow=user_uow, jwt_manager=jwt_manager
    )

    delete_user_usecase = providers.Factory(
        DeleteUserUseCase,
        uow=user_uow,
        logout_usecase=logout_usecase,
        authorize_usecase=authorize_usecase,
    )

    # ==== Factory ====

    register_factory = providers.Factory(RegisterUseCase).provider
