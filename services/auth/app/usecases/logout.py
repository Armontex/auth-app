from ..ports import IJWTManager


class LogoutUseCase:

    def __init__(
        self,
        jwt_manager: IJWTManager,
    ) -> None:
        self._jwt = jwt_manager

    async def execute(self, token: str) -> None:
        """
        Raises:
            TokenVerifyError: Неверный, истёкший или отозванный токен.
        """
        await self._jwt.revoke(token)
