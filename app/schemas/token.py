from enum import Enum

from pydantic import BaseModel


class TokenEnum(str, Enum):
    ACCESS_TOKEN = "access_token"
    REFRESH_TOKEN = "refresh_token"


class TokenPayload(BaseModel):
    sub: int
    exp: float
    username: str
    type: TokenEnum


class RefreshRequest(BaseModel):
    refresh_token: str
