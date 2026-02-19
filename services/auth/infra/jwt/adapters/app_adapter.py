from services.auth.app.ports import IJWTManager
from typing import override
from ..manager import JWTManager


class JWTManagerAdapter(JWTManager, IJWTManager):

    @override
    async def verify(self, token: str) -> int:
        return (await super().verify(token)).sub
