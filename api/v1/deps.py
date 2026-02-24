from fastapi import Header, HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.rbac.domain.const import Permission
from services.auth.app.containers import AuthContainer, AuthorizeUseCase
from services.auth.app.exc import TokenVerifyError
from services.register.app.containers import RegisterContainer
from services.profile.app.containers import ProfileContainer
from services.rbac.app.containers import RbacContainer
from common.ports import IUser

bearer_scheme = HTTPBearer(auto_error=False)


def get_bearer_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    if credentials is None or not credentials.scheme or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided.",
        )

    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        )

    return credentials.credentials


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


def get_rbac_container(request: Request) -> RbacContainer:
    return request.app.state.rbac_container


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
        try:
            user = await usecase.execute(token)

            if not self._has_permission(user):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
            return user
        except TokenVerifyError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=e.args[0]
            ) from e
