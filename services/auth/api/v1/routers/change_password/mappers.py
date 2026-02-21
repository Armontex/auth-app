from services.auth.domain.models import ChangePasswordForm, EmailAddress, Password
from .schemas import ChangePasswordRequest


def map_request_to_form(request: ChangePasswordRequest) -> ChangePasswordForm:
    return ChangePasswordForm(
        email=EmailAddress(request.email),
        password=request.old_password,
        new_password=Password(request.new_password),
    )
