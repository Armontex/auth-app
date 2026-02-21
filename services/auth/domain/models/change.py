from dataclasses import dataclass
from .email import EmailAddress
from .password import Password

from .login import LoginForm


@dataclass(frozen=True)
class ChangePasswordForm(LoginForm):
    new_password: Password


@dataclass(frozen=True)
class ChangeEmailForm(LoginForm):
    new_email: EmailAddress
