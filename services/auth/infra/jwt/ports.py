from typing import Protocol
from services.auth.common.types import UUID


class ITokenRepository(Protocol):

    async def is_revoked(self, jti: UUID) -> bool: ...

    async def revoke_token(self, jti: UUID, expire: float) -> None: ...
