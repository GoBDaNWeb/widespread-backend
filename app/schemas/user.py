from enum import Enum

from pydantic import BaseModel, ConfigDict


class UserRoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"


class UserCredentials(BaseModel):
    username: str
    password: str


class UserFromDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    role: UserRoleEnum
    avatar_url: str | None
