from dataclasses import dataclass
from .email import EmailAddress
from ..utils import VALID_NAME_SYMBOLS, is_empty_string
from ..exc import DomainValidationError


@dataclass(frozen=True)
class RegisterForm:
    MIN_LENGTH_PASSWORD = 8
    MAX_LENGTH_PASSWORD = 128
    MAX_LENGTH_NAME = 100

    first_name: str
    last_name: str
    email: EmailAddress
    password: str
    confirm_password: str
    middle_name: str | None = None

    def __post_init__(self):
        errors: dict[str, list[str]] = {}

        first_name_errors = self.validate_first_name()
        for msg in first_name_errors:
            errors.setdefault("first_name", []).append(msg)

        last_name_errors = self.validate_last_name()
        for msg in last_name_errors:
            errors.setdefault("last_name", []).append(msg)

        middle_name_errors = self.validate_middle_name()
        if middle_name_errors is not None:
            for msg in middle_name_errors:
                errors.setdefault("middle_name", []).append(msg)

        password_errors = self.validate_password()
        for msg in password_errors:
            errors.setdefault("password", []).append(msg)

        confirm_password_errors = self.validate_confirm_password()
        for msg in confirm_password_errors:
            errors.setdefault("confirm_password", []).append(msg)

        if errors:
            raise DomainValidationError(errors)

    def validate_first_name(self) -> list[str]:
        return self.__validate_name(self.first_name)

    def validate_last_name(self) -> list[str]:
        return self.__validate_name(self.last_name)

    def validate_middle_name(self) -> list[str] | None:
        if self.middle_name is not None:
            return self.__validate_name(self.middle_name)

    @classmethod
    def __validate_name(cls, value: str) -> list[str]:
        messages = []

        if is_empty_string(value):
            messages.append("cannot be empty")

        if len(value) > cls.MAX_LENGTH_NAME:
            messages.append(f"too long (max {cls.MAX_LENGTH_NAME})")

        messages.extend(
            f"Invalid character '{char}'"
            for char in value
            if char not in VALID_NAME_SYMBOLS
        )

        return messages

    def validate_password(self) -> list[str]:
        messages = []

        if len(self.password) < self.MIN_LENGTH_PASSWORD:
            messages.append(f"too short (min {self.MIN_LENGTH_PASSWORD})")
        else:
            if self.password[:1].isspace():
                messages.append("cannot start with a space")
            if self.password[-1:].isspace():
                messages.append("cannot end with a space")

        if len(self.password) > self.MAX_LENGTH_PASSWORD:
            messages.append(f"too long (max {self.MAX_LENGTH_PASSWORD})")

        return messages

    def validate_confirm_password(self) -> list[str]:
        messages = []

        if is_empty_string(self.confirm_password):
            messages.append("cannot be empty")

        if self.password != self.confirm_password:
            messages.append("passwords do not match")

        return messages
