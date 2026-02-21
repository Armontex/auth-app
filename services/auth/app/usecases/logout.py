from ..ports import IJWTManager
from ..exc import LogoutError, TokenVerifyError





class LogoutUseCase:

    def __init__(
        self,
        jwt_manager: IJWTManager,
    ) -> None:
        self._jwt = jwt_manager

    async def execute(self, token: str) -> None:
        try:
            await self._jwt.revoke(token)
        except TokenVerifyError as e:
            raise LogoutError(str(e)) from e
