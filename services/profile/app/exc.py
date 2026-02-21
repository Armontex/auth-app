from ..common.exc import AppError


class ProfileAlreadyExists(AppError):

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or "A profile for the user already exists")


class ProfileNotFound(AppError):

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or "Profile not found.")
