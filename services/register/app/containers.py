from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import async_sessionmaker

from common.ports import IPasswordHasher

from .usecases import RegisterUseCase
from .ports import AuthResisterFactory, ProfileRegisterFactory, SetRoleFunc
from .uow import RegisterUoW


class RegisterContainer(containers.DeclarativeContainer):
    session_maker = providers.Dependency(async_sessionmaker)
    password_hasher = providers.Dependency(IPasswordHasher)
    auth_register_factory = providers.Dependency(AuthResisterFactory)
    profile_register_factory = providers.Dependency(ProfileRegisterFactory)
    set_role_func = providers.Dependency(SetRoleFunc)

    register_uow = providers.Factory(RegisterUoW, session_maker=session_maker)

    # ==== UseCases ====

    register_usecase = providers.Factory(
        RegisterUseCase,
        uow=register_uow,
        password_hasher=password_hasher,
        make_auth_register=auth_register_factory,
        make_profile_register=profile_register_factory,
        set_role=set_role_func,
    )
