from dataclasses import dataclass
from .email import EmailAddress
from ..exc import AuthDomainValidationError
from ..utils import is_empty_string


@dataclass(frozen=True)
class LoginForm:
    email: EmailAddress
    password: str

    def __post_init__(self):
        errors: dict[str, list[str]] = {}

        password_errors = self.validate_password()
        for msg in password_errors:
            errors.setdefault("password", []).append(msg)

        if errors:
            raise AuthDomainValidationError(errors)

    def validate_password(self) -> list[str]:
        messages = []

        if is_empty_string(self.password):
            messages.append("cannot be empty")

        return messages
