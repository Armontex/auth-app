from fastapi import Request
from api.v1.deps import validate_content_type
from services.register.app.containers import RegisterContainer


def get_register_container(request: Request) -> RegisterContainer:
    return request.app.state.register_container
