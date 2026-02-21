from typing import Protocol
from datetime import datetime

from common.ports import IUoW, IJWTManager, IPasswordHasher


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

    async def set_password_hash(self, user: IUser, new_password_hash: str) -> None: ...

    async def set_email(self, user: IUser, new_email: str) -> None: ...
