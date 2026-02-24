from typing import Protocol
from services.auth.common.types import UUID


class ITokenRepository(Protocol):

    def is_revoked(self, jti: UUID) -> bool: ...

    def revoke_token(self, jti: UUID, expire: float) -> None: ...
