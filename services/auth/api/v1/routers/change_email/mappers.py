from services.auth.domain.models import ChangeEmailForm, EmailAddress
from .schemas import ChangeEmailRequest


def map_request_to_form(request: ChangeEmailRequest) -> ChangeEmailForm:
    return ChangeEmailForm(
        email=EmailAddress(request.email),
        password=request.password,
        new_email=EmailAddress(request.new_email),
    )
