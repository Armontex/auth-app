from fastapi import HTTPException, status
from ...app.usecases.logout import LogoutError


def map_logout_error(exc: LogoutError) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token.",
    )
