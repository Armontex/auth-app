from ..common.exc import AppError


class RoleNotFound(AppError):

    def __init__(self, role_name: str) -> None:
        super().__init__(f"Role '{role_name}' not found.")


