import jwt
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, UTC
from services.auth.common.types import UUID
from .ports import ITokenRepository

from services.auth.app.exc import TokenVerifyError

@dataclass(frozen=True)
class TokenPayload:
    sub: str
    jti: UUID
    iat: float
    exp: float


# TODO: Добавить refresh_token.
class JWTManager:
    ALGORITHM = "HS256"
    ACCESS_EXPIRES_MINUTES = 60 * 24  # 1 день

    def __init__(self, token_repo: ITokenRepository, secret_key: str) -> None:
        self._token_repo = token_repo
        self._secret_key = secret_key

    def issue_access(self, user_id: int) -> str:
        return self._create_token(user_id, self.ACCESS_EXPIRES_MINUTES)

    async def verify(self, token: str) -> TokenPayload:
        try:
            row_payload = jwt.decode(
                token, self._secret_key, algorithms=[self.ALGORITHM]
            )
            payload = TokenPayload(**row_payload)
        except jwt.InvalidTokenError as e:
            raise TokenVerifyError("Invalid or expired token") from e

        if await self._token_repo.is_revoked(payload.jti):
            raise TokenVerifyError("Revoked token")

        return payload

    async def revoke(self, token: str) -> None:
        payload = await self.verify(token)
        await self._token_repo.revoke_token(payload.jti, payload.exp)

    def _create_token(self, user_id: int, expires_minutes: int) -> str:
        now = datetime.now(UTC)
        exp = now + timedelta(minutes=expires_minutes)

        payload = {
            "sub": str(user_id),
            "jti": str(uuid.uuid4()),
            "iat": now.timestamp(),
            "exp": exp.timestamp(),
        }

        return jwt.encode(payload, key=self._secret_key, algorithm=self.ALGORITHM)
