from typing import override
from datetime import datetime, UTC
from redis_om import NotFoundError, get_redis_connection
from services.auth.infra.jwt.ports import ITokenRepository
from services.auth.common.types import UUID
from .models import RevokedToken


class TokenRepositoryRedis(ITokenRepository):

    def __init__(self, url: str | None = None) -> None:
        self._conn = get_redis_connection(url=url) if url else get_redis_connection()

    def _bind(self):
        setattr(RevokedToken.Meta, "database", self._conn)

    @override
    def revoke_token(self, jti: UUID, expire: float) -> None:
        self._bind()

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
        self._bind()
        try:
            RevokedToken.get(jti)
            return True
        except NotFoundError:
            return False
