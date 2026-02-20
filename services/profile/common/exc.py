class ProfileError(Exception):
    pass

class DomainError(ProfileError):
    pass

class InfraError(ProfileError):
    pass

class AppError(ProfileError):
    pass