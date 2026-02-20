from .schemas import RegisterRequests, RegisterResponse, LoginRequests, LoginResponse
from ...domain.models import EmailAddress, LoginForm
from ...domain.models import RegisterForm as UserRegisterForm
from ...app.ports import IUser

from services.profile.domain.models import RegisterForm as ProfileRegisterForm
from services.profile.domain.models import Name


def map_user_to_response(user: IUser) -> RegisterResponse:
    return RegisterResponse(id=user.id, email=user.email)


def map_register_request_to_form(
    request: RegisterRequests,
) -> tuple[UserRegisterForm, ProfileRegisterForm]:
    return (
        UserRegisterForm(
            email=EmailAddress(str(request.email)),
            password=request.password,
            confirm_password=request.confirm_password,
        ),
        ProfileRegisterForm(
            first_name=Name(request.first_name),
            middle_name=Name(request.middle_name) if request.middle_name else None,
            last_name=Name(request.last_name),
        ),
    )


def map_login_request_to_form(request: LoginRequests) -> LoginForm:
    return LoginForm(email=EmailAddress(request.email), password=request.password)


def map_token_to_response(token: str) -> LoginResponse:
    return LoginResponse(access_token=token)
