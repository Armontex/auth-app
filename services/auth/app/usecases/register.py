from common.exc import RepositoryError
from ..ports import IRegisterUoW, IUser, IPasswordHasher
from .exc import AppError
from ...domain.models import RegisterForm

from services.profile.domain.models import RegisterForm as ProfileRegisterForm


class RegisterError(AppError): ...


class RegisterUseCase:

    def __init__(self, uow: IRegisterUoW, password_hasher: IPasswordHasher) -> None:
        self._uow = uow
        self._hasher = password_hasher

    async def execute(
        self, user_form: RegisterForm, profile_form: ProfileRegisterForm
    ) -> IUser:
        try:
            async with self._uow as (user_repo, profile_repo):
                user = await user_repo.add(
                    email=user_form.email.value,
                    password_hash=self._hasher.hash(user_form.password),
                )
                
                await profile_repo.add(
                    user_id=user.id,
                    first_name=profile_form.first_name.value,
                    middle_name=(
                        profile_form.middle_name.value
                        if profile_form.middle_name
                        else None
                    ),
                    last_name=profile_form.last_name.value,
                )
                return user
        except RepositoryError as e:
            raise RegisterError(str(e)) from e
