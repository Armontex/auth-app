from dataclasses import dataclass
from .email import EmailAddress


@dataclass(frozen=True)
class LoginForm:
    email: EmailAddress
    password: str
