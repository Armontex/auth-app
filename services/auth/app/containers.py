from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from config.settings import settings

from .ports import IJWTManager, IPasswordHasher
from .usecases import RegisterUseCase, LoginUseCase, LogoutUseCase, DeleteUserUseCase
from .uow.user import UserUoW, IUserUoW

from ..infra.db.tokens.repos import ITokenRepository, TokenRepositoryRedis
from ..infra.jwt.adapters.app_adapter import JWTManagerAdapter
from ..infra.security.hasher import PasswordHasher


class AuthContainer(containers.DeclarativeContainer):
    session_maker = providers.Dependency(instance_of=async_sessionmaker)

    wiring_config = containers.WiringConfiguration(
        modules=["services.auth.api.v1.routers"]
    )

    # ==== Infra ====

    redis_token_repo = providers.Singleton[ITokenRepository](
        TokenRepositoryRedis, url=settings.redis_url
    )

    user_uow = providers.Factory[IUserUoW](UserUoW, session_factory=session_maker)

    jwt_manager = providers.Singleton[IJWTManager](
        JWTManagerAdapter,
        token_repo=redis_token_repo,
        secret_key=settings.secret_key.get_secret_value(),
    )

    password_hasher = providers.Singleton[IPasswordHasher](PasswordHasher)

    # ==== UseCases ====

    register_usecase = providers.Factory(
        RegisterUseCase, uow=user_uow, password_hasher=password_hasher
    )

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

    delete_user_usecase = providers.Factory(
        DeleteUserUseCase,
        uow=user_uow,
        jwt_manager=jwt_manager,
    )
