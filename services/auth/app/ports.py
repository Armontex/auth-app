from typing import Protocol


class IUser(Protocol):
    id: int
    email: str


class IUserRepository(Protocol):

    # async def get_user_by_email(self, email: str) -> IUser | None: ...

    async def add_user(
        self,
        first_name: str,
        middle_name: str | None,
        last_name: str,
        email: str,
        password_hash: str,
    ) -> IUser: ...


class IPasswordHasher(Protocol):

    def hash(self, password: str) -> str: ...

    def verify(self, password: str, password_hash: str) -> bool: ...
