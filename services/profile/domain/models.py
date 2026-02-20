from dataclasses import dataclass
from .utils import is_empty_string, VALID_NAME_SYMBOLS
from .const import NAME_MAX_LENGTH
from .exc import DomainValidationError


@dataclass
class Name:
    value: str

    def __post_init__(self):
        errors: dict[str, list[str]] = {}

        value_messages = self._validate_value()
        if value_messages:
            errors.setdefault("value", []).extend(value_messages)

        if errors:
            raise DomainValidationError(errors)

    def _validate_value(self) -> list[str]:
        messages = []

        if is_empty_string(self.value):
            messages.append("cannot be empty")

        if len(self.value) > NAME_MAX_LENGTH:
            messages.append(f"too long (max {NAME_MAX_LENGTH})")

        messages.extend(
            f"Invalid character '{char}'"
            for char in self.value
            if char not in VALID_NAME_SYMBOLS
        )

        return messages


@dataclass(frozen=True)
class RegisterForm:
    first_name: Name
    middle_name: Name | None
    last_name: Name


@dataclass(frozen=True)
class UpdateForm:
    first_name: Name | None
    middle_name: Name | None
    last_name: Name | None
