from dataclasses import dataclass
from email_validator import validate_email, EmailNotValidError
from ..exc import DomainValidationError


@dataclass(frozen=True)
class EmailAddress:
    value: str

    def __post_init__(self):
        try:
            value = self.value.strip().lower()
            res = validate_email(value, check_deliverability=False)
        except EmailNotValidError as e:
            raise DomainValidationError({"email": ["Invalid email address"]}) from e
        
        object.__setattr__(self, "value", res.normalized)
