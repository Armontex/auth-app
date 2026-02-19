from ..ports import IJWTManager
from .exc import AppError
from services.auth.common.exc import InfraError


class LogoutError(AppError): ...


class LogoutUseCase:

    def __init__(
        self,
        jwt_manager: IJWTManager,
    ) -> None:
        self._jwt = jwt_manager

    async def execute(self, token: str) -> None:
        try:
            await self._jwt.revoke(token)
        except InfraError as e:
            raise LogoutError("Invalid or expired token") from e
