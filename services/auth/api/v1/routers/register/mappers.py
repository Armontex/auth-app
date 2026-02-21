from .schemas import RegisterRequests, RegisterResponse
from services.auth.domain.models import EmailAddress, Password, RegisterForm
from services.auth.app.ports import IUser


def map_user_to_response(user: IUser) -> RegisterResponse:
    return RegisterResponse(id=user.id, email=user.email)
