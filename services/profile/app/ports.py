from typing import Protocol, TYPE_CHECKING

from common.ports import IUoW, IJWTManager, IPasswordHasher

if TYPE_CHECKING:
    from services.auth.app.ports import IUser


class IProfile(Protocol):
    id: int
    user_id: int
    first_name: str
    middle_name: str | None
    last_name: str
    user: "IUser"


class IProfileRepository(Protocol):

    async def add(
        self,
        user_id: int,
        first_name: str,
        middle_name: str | None,
        last_name: str,
    ) -> IProfile: ...

    async def get_by_user_id(self, user_id: int) -> IProfile | None: ...

    async def set_first_name(self, profile: IProfile, new_first_name: str) -> None: ...
    async def set_last_name(self, profile: IProfile, new_last_name: str) -> None: ...
    async def set_middle_name(
        self, profile: IProfile, new_middle_name: str | None
    ) -> None: ...
