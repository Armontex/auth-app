from typing import Protocol, runtime_checkable
from datetime import datetime


class IUoW[T](Protocol):

    async def __aenter__(self) -> T: ...
    async def __aexit__(self, exc_type, exc, tb): ...


class IJWTManager(Protocol):

    def issue_access(self, user_id: int) -> str: ...
    async def verify(self, token: str) -> int: ...
    async def revoke(self, token: str) -> None: ...


@runtime_checkable
class IPasswordHasher(Protocol):

    def hash(self, password: str) -> str: ...

    def verify(self, password: str, password_hash: str) -> bool: ...


class IUser(Protocol):
    id: int
    email: str
    password_hash: str
    is_active: bool
    created_at: datetime
    profile: "IProfile"
    roles: list["IRole"]


class IProfile(Protocol):
    id: int
    user_id: int
    first_name: str
    middle_name: str | None
    last_name: str
    user: "IUser"


class IRole(Protocol):
    id: int
    name: str
    users: list["IUser"]
    permissions: list["IPermission"]


class IPermission(Protocol):
    id: int
    code: str
    roles: list["IRole"]
