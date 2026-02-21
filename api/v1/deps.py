from fastapi import Header, HTTPException, status


def get_bearer_token(authorization: str | None = Header(default=None)) -> str:

    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided.",
        )

    try:
        scheme, token = authorization.split(" ", 1)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        ) from e

    if scheme.lower() != "bearer" or not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        )

    return token


def validate_content_type(content_type: str = Header(..., alias="Content-Type")):
    if content_type != "application/json":
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Content-Type must be application/json",
        )
