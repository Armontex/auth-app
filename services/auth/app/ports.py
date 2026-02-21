from typing import Protocol, override
from datetime import datetime

from services.profile.app.ports import IProfileRepository


class IUser(Protocol):
    id: int
    email: str
    password_hash: str
    is_active: bool
    created_at: datetime


class IUserRepository(Protocol):

    async def get_user_by_email(self, email: str) -> IUser | None: ...

    async def add(
        self,
        email: str,
        password_hash: str,
    ) -> IUser: ...

    async def delete_user(self, user_id: int) -> None: ...

    async def set_password_hash(
        self, user: IUser, new_password_hash: str
    ) -> None: ...

    async def set_email(self, user: IUser, new_email: str) -> None: ...


class IPasswordHasher(Protocol):

    def hash(self, password: str) -> str: ...

    def verify(self, password: str, password_hash: str) -> bool: ...


class IJWTManager(Protocol):

    def issue_access(self, user_id: int) -> str: ...
    async def verify(self, token: str) -> int: ...
    async def revoke(self, token: str) -> None: ...


class IUoW[T](Protocol):

    async def __aenter__(self) -> T: ...
    async def __aexit__(self, exc_type, exc, tb): ...

