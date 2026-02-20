from .schemas import RegisterRequests, RegisterResponse, LoginRequests, LoginResponse
from ...domain.models import RegisterForm, EmailAddress, LoginForm
from ...app.ports import IUser


def map_user_to_response(user: IUser) -> RegisterResponse:
    return RegisterResponse(id=user.id, email=user.email)


def map_register_request_to_form(request: RegisterRequests) -> RegisterForm:
    return RegisterForm(
        first_name=request.first_name,
        last_name=request.last_name,
        email=EmailAddress(str(request.email)),
        password=request.password,
        confirm_password=request.confirm_password,
    )


def map_login_request_to_form(request: LoginRequests) -> LoginForm:
    return LoginForm(email=EmailAddress(request.email), password=request.password)


def map_token_to_response(token: str) -> LoginResponse:
    return LoginResponse(access_token=token)
