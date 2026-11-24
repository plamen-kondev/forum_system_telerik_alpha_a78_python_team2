from fastapi import APIRouter, Depends, status
from app.common.auth import get_current_user
from app.models.user import User, UserLogin, UserOut, UserRegister, TokenOut
from app.services import auth_service

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Creates a new account. Username and email must be unique. Password is stored as a bcrypt hash.",
)
def register(data: UserRegister):
    user = auth_service.register(data)
    return UserOut.from_user(user)


@router.post(
    "/login",
    response_model=TokenOut,
    summary="Log in and get an access token",
    description="Returns a JWT. Send it as `Authorization: Bearer <token>` on protected endpoints.",
)
def login(data: UserLogin):
    token = auth_service.login(data)
    return TokenOut(access_token=token)


@router.get(
    "/me",
    response_model=UserOut,
    summary="Get the currently logged-in user",
)
def me(user: User = Depends(get_current_user)):
    return UserOut.from_user(user)