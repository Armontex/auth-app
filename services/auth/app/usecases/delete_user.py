from ..ports import IJWTManager, IUserRepository
from .exc import AppError
from common.exc import RepositoryError
from services.auth.common.exc import InfraError


class DeleteUserError(AppError): ...


class DeleteUserErrorUseCase:

    def __init__(
        self,
        user_repo: IUserRepository,
        jwt_manager: IJWTManager,
    ) -> None:
        self._user_repo = user_repo
        self._jwt = jwt_manager

    async def execute(self, token: str) -> None:
        try:
            user_id = await self._jwt.verify(token)
            await self._jwt.revoke(token)
            await self._user_repo.delete_user(user_id)
        except InfraError as e:
            raise DeleteUserError("Invalid or expired token") from e
        except RepositoryError as e:
            raise DeleteUserError("This user does not exist") from e
