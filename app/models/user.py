from datetime import datetime
from enum import Enum
from typing import Annotated
from pydantic import BaseModel, EmailStr, Field, StringConstraints

class Role(str, Enum):
    USER = 'user'
    ADMIN = 'admin'

#preizpolzvaemi field types s pravilata ot uslovieto

Name = Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=32)]
Username = Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=16, pattern = r"^[A-Za-z0-9_.]+$")]
Password = Annotated[str, StringConstraints(min_length=8, max_length=72)]

#kakvo podava klienta
class UserRegister(BaseModel):
    first_name: Name
    last_name: Name
    email: EmailStr
    username: Username
    password: Password


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    first_name: Name | None = None
    last_name: Name | None = None
    email: EmailStr | None = None

#ne se vrushta(internal object)
class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    username: str
    password_hash: str
    role: Role
    is_blocked: bool
    created_at: datetime

    @property
    def is_admin(self)->bool:
        return self.role == Role.ADMIN

    @classmethod
    def from_row(cls, row: tuple) -> "User":
#konventira db row v User. Order-a na kolonite trqbva da matchva Select-a v repositorito.
        id, first_name, last_name, email, username, password_hash, role, is_blocked, created_at = row
        return cls(
            id=id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password_hash=password_hash,
            role=role,
            is_blocked=bool(is_blocked),
            created_at=created_at
        )

#kakvo vrushta api-to
class UserOut(BaseModel):
    #Celiq profil koito se pokazva na user-a i na admin-a
    id: int
    first_name: str
    last_name: str
    email: str
    username: str
    role: Role
    is_blocked: bool
    created_at: datetime

    @classmethod
    def from_user(cls, user: User) -> "UserOut":
        return cls(**user.model_dump(exclude={"password_hash"}))

class UserPublic(BaseModel): #kakvo vijdat drugite user-i bez personal info
    id:int
    username: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = 'bearer'


