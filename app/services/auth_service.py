from datetime import datetime, timedelta, timezone
import bcrypt
from jose import jwt, JWTError
from app import config
from app.common.exceptions import ConflictError, UnauthorizedError
from app.models.user import User, UserRegister, UserLogin
from app.repositories import user_repository

ALGORITHM = 'HS256'

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def create_access_token(user: User) -> str:
    # The token stores only the user id ("sub") and an expiry time ("exp").
    # It is signed with JWT_SECRET, so nobody can change it without the secret.
    expires_at = datetime.now(timezone.utc) + timedelta(minutes = config.JWT_EXPIRE_MINUTES)
    payload = {'sub': str(user.id), 'exp': expires_at}
    return jwt.encode(payload, config.JWT_SECRET, algorithm=ALGORITHM)

def get_user_from_token(token: str) -> User:
    try:
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=[ALGORITHM])
        user_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        # Covers: fake token, wrong signature, expired token, missing/bad "sub"
        raise UnauthorizedError("Invalid or expired token")

    user = user_repository.get_by_id(user_id)
    if user is None:
        raise UnauthorizedError("Invalid or expired token")
    return user

def register(data: UserRegister) -> User | None:
    if user_repository.get_by_username(data.username) is not None:
        raise ConflictError("Username is already taken")
    if user_repository.get_by_email(data.email) is not None:
        raise ConflictError("Email is already registered")
    user_id = user_repository.create(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        username=data.username,
        password_hash=hash_password(data.password),
    )
    return user_repository.get_by_id(user_id)


def login(data: UserLogin) -> str:
    user = user_repository.get_by_username(data.username)
    if user is None or not verify_password(data.password, user.password_hash):
        raise UnauthorizedError("Invalid username or password")
    return create_access_token(user)


