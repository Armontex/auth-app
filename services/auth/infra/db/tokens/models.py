from redis_om import HashModel
from typing import Literal
from services.auth.common.types import UUID


class RevokedToken(HashModel):
    jti: UUID

    class Meta:
        global_key_prefix = "blacklist"
