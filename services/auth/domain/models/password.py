from dataclasses import dataclass
from ..const import PASSWORD_MAX_LENGTH, PASSWORD_MIN_LENGTH
from ..exc import ValidationError


@dataclass(frozen=True)
class Password:
    value: str

    def __post_init__(self):
        errors: dict[str, list[str]] = {}

        value_messages = self._validate_value()
        if value_messages:
            errors.setdefault("password", []).extend(value_messages)

        if errors:
            raise ValidationError(errors)

    def _validate_value(self) -> list[str]:
        messages = []

        if len(self.value) < PASSWORD_MIN_LENGTH:
            messages.append(f"too short (min {PASSWORD_MIN_LENGTH})")
        else:
            if self.value[:1].isspace():
                messages.append("cannot start with a space")
            if self.value[-1:].isspace():
                messages.append("cannot end with a space")

        if len(self.value) > PASSWORD_MAX_LENGTH:
            messages.append(f"too long (max {PASSWORD_MAX_LENGTH})")

        return messages
