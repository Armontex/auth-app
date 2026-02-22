from ..ports import IProfileRepository

from ...domain.models import RegisterForm


class RegisterUseCase:

    def __init__(self, repo: IProfileRepository) -> None:
        self._repo = repo

    async def execute(self, user_id: int, form: RegisterForm) -> None:
        """
        Raises:
            ProfileAlreadyExists: Профиль с таким `user_id` уже существует.
        """
        await self._repo.add(
            user_id=user_id,
            first_name=form.first_name.value,
            middle_name=form.middle_name.value if form.middle_name else None,
            last_name=form.last_name.value,
        )
