from .schemas import RegisterRequests, RegisterResponse
from common.ports import IUser
from services.auth.domain.models.register import (
    RegisterForm as AuthRegisterForm,
    EmailAddress,
    Password,
)
from services.profile.domain.models import RegisterForm as ProfileRegisterForm, Name


def map_user_to_response(user: IUser) -> RegisterResponse:
    return RegisterResponse(id=user.id, email=user.email)


def map_request_to_auth_form(request: RegisterRequests) -> AuthRegisterForm:
    return AuthRegisterForm(
        email=EmailAddress(request.email),
        password=Password(request.password),
        confirm_password=request.confirm_password,
    )


def map_request_to_profile_form(request: RegisterRequests) -> ProfileRegisterForm:
    return ProfileRegisterForm(
        first_name=Name(request.first_name),
        last_name=Name(request.last_name),
        middle_name=Name(request.middle_name) if request.middle_name else None,
    )
