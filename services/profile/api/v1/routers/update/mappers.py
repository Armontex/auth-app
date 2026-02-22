from .schemas import UpdateRequest, UpdateResponse

from services.profile.domain.models import UpdateForm, Name
from common.ports import IProfile


def map_request_to_form(request: UpdateRequest) -> UpdateForm:
    first_name = Name(request.first_name) if request.first_name else None
    last_name = Name(request.last_name) if request.last_name else None
    middle_name = Name(request.middle_name) if request.middle_name else None
    return UpdateForm(
        first_name=first_name, middle_name=middle_name, last_name=last_name
    )


def map_profile_to_response(profile: IProfile) -> UpdateResponse:
    return UpdateResponse(
        first_name=profile.first_name,
        last_name=profile.last_name,
        middle_name=profile.middle_name,
    )
