from ..common.exc import DomainError


class ValidationError(DomainError):

    def __init__(self, errors: dict[str, list[str]]) -> None:
        self.errors = errors
        super().__init__(f"Validation errors: {errors}")
