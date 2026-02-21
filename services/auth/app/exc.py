from ..common.exc import AppError

class LoginError(AppError):

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or "Invalid credentials.")


class EmailAlreadyExists(AppError):

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or "Email already exists.")


class UserNotExists(AppError):

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or "User does not exists.")


class TokenVerifyError(AppError): ...
