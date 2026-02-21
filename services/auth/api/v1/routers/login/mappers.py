from services.auth.domain.models import EmailAddress, LoginForm
from .schemas import LoginRequests, LoginResponse


def map_login_request_to_form(request: LoginRequests) -> LoginForm:
    return LoginForm(email=EmailAddress(request.email), password=request.password)


def map_token_to_response(token: str) -> LoginResponse:
    return LoginResponse(access_token=token)
