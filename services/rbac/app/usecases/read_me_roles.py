from common.ports import IUser, IRole


class ReadMeRolesUseCase:

    def execute(self, user: IUser) -> list[IRole]:
        return user.roles
