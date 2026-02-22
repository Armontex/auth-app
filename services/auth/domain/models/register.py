from dataclasses import dataclass
from .email import EmailAddress
from .password import Password
from ..exc import ValidationError


@dataclass(frozen=True)
class RegisterForm:
    email: EmailAddress
    password: Password
    confirm_password: str

    def __post_init__(self):
        errors: dict[str, list[str]] = {}

        confirm_password_messages = self._validate_confirm_password()
        if confirm_password_messages:
            errors.setdefault("password", []).extend(confirm_password_messages)

        if errors:
            raise ValidationError(errors)

    def _validate_confirm_password(self) -> list[str]:
        messages = []

        if self.password.value != self.confirm_password:
            messages.append("passwords do not match")

        return messages
