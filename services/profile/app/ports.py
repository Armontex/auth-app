from typing import Protocol


class IProfile(Protocol):
    id: int
    first_name: str
    middle_name: str | None
    last_name: str


class IProfileRepository(Protocol):

    async def add(
        self,
        user_id: int,
        first_name: str,
        middle_name: str | None,
        last_name: str,
    ) -> IProfile: ...


class IProfileUoW(Protocol):

    async def __aenter__(self) -> IProfileRepository: ...
    async def __aexit__(self, exc_type, exc, tb): ...
