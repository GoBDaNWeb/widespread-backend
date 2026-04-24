import hashlib
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.schemas.token import TokenEnum, TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(12))
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def encode_jwt(token: TokenPayload) -> str:
    token_expire = datetime.now(timezone.utc) + timedelta(minutes=token.exp)

    token_payload = {
        "sub": str(token.sub),
        "exp": token_expire,
        "username": token.username,
        "type": token.type,
    }

    return jwt.encode(token_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_jwt(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return TokenPayload.model_validate(payload)
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(status_code=401, detail="Token expired") from e
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail="Invalid token") from e


def create_jwt(user_id: int, username: str):
    access_token = encode_jwt(
        TokenPayload(
            sub=user_id,
            username=username,
            exp=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            type=TokenEnum.ACCESS_TOKEN,
        )
    )

    refresh_token = encode_jwt(
        TokenPayload(
            sub=user_id,
            username=username,
            exp=settings.REFRESH_TOKEN_EXPIRE_MINUTES,
            type=TokenEnum.REFRESH_TOKEN,
        )
    )

    return {"access_token": access_token, "refresh_token": refresh_token}


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
