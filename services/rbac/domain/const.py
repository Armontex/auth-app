from enum import Enum


# IDEA: Перенести в yaml и загружать в InitRbac с конфига
class Permission(str, Enum):
    # ==== PROFILE ====
    PROFILE_ME_READ = "profile:me:read"  # смотреть свой профиль
    PROFILE_ME_UPDATE = "profile:me:update"  # редактировать свой профиль

    PROFILE_READ = "profile:read"  # смотреть чужие профили
    PROFILE_UPDATE = "profile:update"  # редактировать чужие профили

    # ==== ROLES ====
    ROLE_ME_READ = "role:me:read"  # смотреть свои роли # [x]: usecase | # [ ]: router
    ROLE_READ = "role:read"  # смотреть роли других # [x]: usecase | # [ ]: router
    ROLE_SET = "role:set"  # назначать роли другим # [x]: usecase | # [ ]: router

    # ==== PERMISSIONS ====
    PERMISSION_ME_READ = (
        "permission:me:read"  # смотреть свои разрешения # [x]: usecase | # [ ]: router
    )
    PERMISSION_READ = (
        "permission:read"  # смотреть чужие разрешения # [x]: usecase | # [ ]: router
    )


class Role(str, Enum):
    LIMITED_USER = "limited_user"
    USER = "user"
    ADMIN = "admin"


# ==== Группы ====

PROFILE_ME_PERMISSIONS = {
    Permission.PROFILE_ME_READ,
    Permission.PROFILE_ME_UPDATE,
}

PROFILE_PERMISSIONS = {
    Permission.PROFILE_READ,
    Permission.PROFILE_UPDATE,
}

# ROLE_PERMISSIONS_PERMISSIONS = {
#     Permission.ROLE_ME_READ,
#     Permission.ROLE_READ,
#     Permission.ROLE_SET,
# }

# PERMISSION_PERMISSIONS = {
#     Permission.PERMISSION_ME_READ,
#     Permission.PERMISSION_READ,
# }


ROLE_PERMISSIONS = {
    Role.LIMITED_USER: [Permission.PROFILE_ME_READ],
    Role.USER: PROFILE_ME_PERMISSIONS,
    Role.ADMIN: set(Permission),
}
