from typing import override
from services.auth.infra.jwt.ports import ITokenRepository
from datetime import datetime, UTC
from services.auth.common.types import UUID
from .models import RevokedToken


class TokenRepositoryRedis(ITokenRepository):

    @override
    def revoke_token(self, jti: UUID, expire: float) -> None:

        now = datetime.now(UTC)
        delta = datetime.fromtimestamp(expire, UTC) - now
        ttl = int(delta.total_seconds())
        if ttl <= 0:
            return

        token = RevokedToken(pk=jti, jti=jti)
        token.save()
        token.expire(ttl)

    @override
    def is_revoked(self, jti: UUID) -> bool:
        return RevokedToken.get(jti) is not None
