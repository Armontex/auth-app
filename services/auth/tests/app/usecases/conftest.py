import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime, timedelta, UTC

from services.auth.app.ports import (
    IUser,
    IUserRepository,
    IUserUoW,
    IPasswordHasher,
    IJWTManager,
    IRegisterUoW,
)
from services.profile.app.ports import IProfileRepository
from services.profile.domain.models import Name


# ==== IUser ====


@pytest.fixture
def user() -> IUser:
    now = datetime.now(UTC) - timedelta(days=30)
    u = Mock()
    u.id = 42
    u.email = "test@example.com"
    u.password_hash = "hashed_password"
    u.is_active = True
    u.created_at = now
    return u


# ==== IUserRepository ====


@pytest.fixture
def user_repo(user) -> IUserRepository:
    repo = AsyncMock()
    repo.get_user_by_email = AsyncMock(return_value=user)
    repo.add = AsyncMock(return_value=user)  # новое имя метода
    repo.delete_user = AsyncMock(return_value=None)
    return repo


# ==== IProfileRepository ====


@pytest.fixture
def profile_repo() -> IProfileRepository:
    repo = AsyncMock()
    repo.add = AsyncMock(return_value=None)
    return repo


# ==== IUserUoW ==== (для старых use-case’ов login/logout/delete и т.п.)


@pytest.fixture
def user_uow(user_repo) -> IUserUoW:
    uow = AsyncMock()
    uow.__aenter__.return_value = user_repo
    uow.__aexit__.return_value = False
    return uow


# ==== IRegisterUoW ==== (для RegisterUseCase, который создаёт user + profile)


@pytest.fixture
def register_uow(user_repo, profile_repo) -> IRegisterUoW:
    uow = AsyncMock()
    # async with uow as (user_repo, profile_repo):
    uow.__aenter__.return_value = (user_repo, profile_repo)
    uow.__aexit__.return_value = False
    # удобный доступ в тестах
    uow.user_repo = user_repo
    uow.profile_repo = profile_repo
    return uow


# ==== IPasswordHasher ====


@pytest.fixture
def password_hasher() -> IPasswordHasher:
    hasher = Mock()
    hasher.hash = Mock(side_effect=lambda p: f"hashed-{p}")
    hasher.verify = Mock(return_value=True)
    return hasher


# ==== IJWTManager ====


@pytest.fixture
def jwt_manager() -> IJWTManager:
    jwt = Mock()
    jwt.issue_access = Mock(return_value="access-token-123")
    jwt.verify = AsyncMock(return_value=42)
    jwt.revoke = AsyncMock(return_value=None)
    return jwt
