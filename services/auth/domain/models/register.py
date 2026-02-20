from dataclasses import dataclass
from .email import EmailAddress
from ..utils import is_empty_string
from ..exc import DomainValidationError
from ..const import PASSWORD_MAX_LENGTH, PASSWORD_MIN_LENGTH


@dataclass(frozen=True)
class RegisterForm:
    email: EmailAddress
    password: str
    confirm_password: str

    def __post_init__(self):
        errors: dict[str, list[str]] = {}

        def add(field: str, msgs: list[str] | None):
            if not msgs:
                return
            errors.setdefault(field, []).extend(msgs)

        add("password", self._validate_password())
        add("confirm_password", self._validate_confirm_password())

        if errors:
            raise DomainValidationError(errors)

    def _validate_password(self) -> list[str]:
        messages = []

        if len(self.password) < PASSWORD_MIN_LENGTH:
            messages.append(f"too short (min {PASSWORD_MIN_LENGTH})")
        else:
            if self.password[:1].isspace():
                messages.append("cannot start with a space")
            if self.password[-1:].isspace():
                messages.append("cannot end with a space")

        if len(self.password) > PASSWORD_MAX_LENGTH:
            messages.append(f"too long (max {PASSWORD_MAX_LENGTH})")

        return messages

    def _validate_confirm_password(self) -> list[str]:
        messages = []

        if is_empty_string(self.confirm_password):
            messages.append("cannot be empty")

        if self.password != self.confirm_password:
            messages.append("passwords do not match")

        return messages
