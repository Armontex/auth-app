class AuthError(Exception):
    pass


class AppError(AuthError):
    pass


class InfraError(AuthError):
    pass


class DomainError(AuthError):
    pass
