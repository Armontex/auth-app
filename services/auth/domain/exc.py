class AuthDomainError(Exception):
    pass


class AuthDomainValidationError(AuthDomainError):

    def __init__(self, errors: dict[str, list[str]]) -> None:
        self.errors = errors
        super().__init__(f"Validation errors: {errors}")
