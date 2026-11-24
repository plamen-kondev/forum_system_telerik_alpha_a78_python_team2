from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.common.exceptions import ForbiddenError, UnauthorizedError
from app.models.user import User
from app.services import auth_service


AUTH_COOKIE_NAME = "access_token"

# Reads "Authorization: Bearer <token>" and adds the "Authorize" button in Swagger.
# auto_error=False -> if the header is missing we don't fail here, we check the cookie next.
bearer_scheme = HTTPBearer(auto_error=False)

def _extract_token(request: Request, credentials: HTTPAuthorizationCredentials | None) -> HTTPAuthorizationCredentials | str | None:
    if credentials is not None:
        return credentials.credentials
    return request.cookies.get(AUTH_COOKIE_NAME)


def get_current_user(
    request: Request, credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)) -> User:
    """polzvai na endpoints koito iskat login. raises 401 ako ne si lognat"""
    token = _extract_token(request, credentials)
    if token is None:
        raise UnauthorizedError("Not authenticated")
    return auth_service.get_user_from_token(token)


def get_optional_user(
    request: Request, credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)) -> User | None:
    """polvai na public pages: vrushta user-a ako e lognat, inache None"""
    token = _extract_token(request, credentials)
    if token is None:
        return None
    try:
        return auth_service.get_user_from_token(token)
    except UnauthorizedError:
        return None


def require_admin(user: User = Depends(get_current_user)) -> User:
    """polzvai na admin endpointi"""
    if not user.is_admin:
        raise ForbiddenError("Admin access required")
    return user


def require_not_blocked(user: User = Depends(get_current_user)) -> User:
    """polzvai na endpoint koito suzdava content. Blokirani useri vrushta 403"""
    if user.is_blocked:
        raise ForbiddenError("Your account is blocked")
    return user