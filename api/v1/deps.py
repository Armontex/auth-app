from typing import Any

from fastapi import Header, HTTPException, status, Depends, Request
from services.rbac.domain.const import Permission
from services.auth.app.containers import AuthContainer, AuthorizeUseCase
from services.register.app.containers import RegisterContainer
from services.profile.app.containers import ProfileContainer
from common.ports import IUser


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


def get_auth_container(request: Request) -> AuthContainer:
    return request.app.state.auth_container


def get_register_container(request: Request) -> RegisterContainer:
    return request.app.state.register_container


def get_profile_container(request: Request) -> ProfileContainer:
    return request.app.state.profile_container


def get_authorize_usecase(
    container: AuthContainer = Depends(get_auth_container),
) -> AuthorizeUseCase:
    return container.authorize_usecase()


class RequirePermission:

    def __init__(self, permission: Permission) -> None:
        self._perm = permission

    def _has_permission(self, user: IUser) -> bool:
        return any(
            perm.code == self._perm.value
            for role in user.roles
            for perm in role.permissions
        )

    async def __call__(
        self,
        token: str = Depends(get_bearer_token),
        usecase: AuthorizeUseCase = Depends(get_authorize_usecase),
    ) -> IUser:
        user = await usecase.execute(token)

        if not self._has_permission(user):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        return user
