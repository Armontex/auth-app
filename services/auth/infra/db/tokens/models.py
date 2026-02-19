from redis_om import HashModel
from services.auth.common.types import UUID


class RevokedToken(HashModel, index=True):
    jti: UUID

    class Meta:
        global_key_prefix = "blacklist"
