from common.ports import IUser, IProfile


class ReadMeProfileUseCase:

    def execute(self, user: IUser) -> IProfile:
        return user.profile
