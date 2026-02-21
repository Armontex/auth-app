from fastapi import Request
from api.v1.deps import validate_content_type, get_bearer_token
from ...app.containers import AuthContainer


def get_auth_container(request: Request) -> AuthContainer:
    return request.app.state.auth_container
