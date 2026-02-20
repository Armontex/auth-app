from ..ports import IJWTManager, IUserUoW
from .exc import AppError
from common.exc import RepositoryError
from services.auth.common.exc import InfraError


class DeleteUserError(AppError): ...

class DeleteUserNotExistsError(DeleteUserError): ...


class DeleteUserUseCase:

    def __init__(
        self,
        uow: IUserUoW,
        jwt_manager: IJWTManager,
    ) -> None:
        self._uow = uow
        self._jwt = jwt_manager

    async def execute(self, token: str) -> None:
        try:
            user_id = await self._jwt.verify(token)
            await self._jwt.revoke(token)

            async with self._uow as repo:
                await repo.delete_user(user_id)

        except InfraError as e:
            raise DeleteUserError("Invalid or expired token") from e
        except RepositoryError as e:
            raise DeleteUserNotExistsError("This user does not exist") from e
