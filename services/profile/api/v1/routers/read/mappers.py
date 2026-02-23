from common.ports import IProfile
from .schemas import ProfileResponse


def map_prof_to_response(prof: IProfile) -> ProfileResponse:
    return ProfileResponse(
        first_name=prof.first_name,
        last_name=prof.last_name,
        middle_name=prof.middle_name,
    )
