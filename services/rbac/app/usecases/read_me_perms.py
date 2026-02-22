from common.ports import IUser, IPermission


class ReadMePermissionsUseCase:

    def execute(self, user: IUser) -> set[IPermission]:
        return {perm for role in user.roles for perm in role.permissions}
