from fastapi import HTTPException, Response
from datetime import datetime, timedelta, timezone

from app.core.config import settings
from app.core.security import create_jwt, decode_jwt, verify_password
from app.schemas.token import TokenEnum
from app.schemas.user import UserCredentials, UserFromDB


class AuthService:
    def __init__(self, user_repo, token_repo):
        self.user_repo = user_repo
        self.token_repo = token_repo

    async def _set_jwt_tokens(self, response: Response, user_id: int, username: str):
        tokens = create_jwt(user_id, username)
        await self.token_repo.save_refresh_token(user_id, tokens["refresh_token"])
        response.set_cookie(
            key="refresh_token",
            value=tokens["refresh_token"],
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=15 * 24 * 3600,
            partitioned=False,
        )

        response.set_cookie(
            key="access_token",
            value=tokens["access_token"],
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=15 * 60,
            partitioned=False,
        )

        return tokens

    async def register(self, user_credentials: UserCredentials):
        new_user = await self.user_repo.register(user_credentials)

        if new_user is None:
            raise HTTPException(status_code=400, detail="User already exists")

        return new_user

    async def login(self, response: Response, user_credentials: UserCredentials):
        existing_user = await self.user_repo.login(user_credentials)

        if existing_user is None:
            raise HTTPException(status_code=403, detail="Invalid credentials")

        correct_password = verify_password(user_credentials.password, existing_user.password)

        if not correct_password:
            raise HTTPException(status_code=403, detail="Invalid credentials")

        user_response = UserFromDB.model_validate(existing_user)

        await self._set_jwt_tokens(response, user_response.id, user_response.username)

        return {"user": user_response}

    async def logout(self, response: Response, refresh_token: str):
        if not refresh_token:
            raise HTTPException(status_code=400, detail="No refresh token provided")

        await self.token_repo.delete_refresh_token(refresh_token)

        response.delete_cookie("refresh_token")
        response.delete_cookie("access_token")

        return {"detail": "Successfully logged out"}

    async def refresh_token(self, response: Response, refresh_token: str):
        if not refresh_token:
            raise HTTPException(
                status_code=401,
                detail="Refresh token missing",
            )
        payload = decode_jwt(refresh_token)

        if payload.type != TokenEnum.REFRESH_TOKEN:
            raise HTTPException(status_code=400, detail="Invalid refresh token")

        token_from_db = await self.token_repo.get_refresh_token(refresh_token)

        if not token_from_db:
            raise HTTPException(status_code=404, detail="Refresh token does not exist")

        if token_from_db.rotated_at is not None:
            grace_period = timedelta(seconds=settings.REFRESH_TOKEN_REUSE_GRACE_SECONDS)

            if datetime.now(timezone.utc) - token_from_db.rotated_at > grace_period:
                await self.token_repo.revoke_user_tokens(token_from_db.user_id)
                raise HTTPException(status_code=401, detail="Refresh token already used")

            active_token = await self.token_repo.get_active_refresh_token(token_from_db.user_id)

            if not active_token:
                raise HTTPException(status_code=401, detail="Session expired")

            token_from_db = active_token

        await self.token_repo.mark_rotated(token_from_db)

        tokens = await self._set_jwt_tokens(response, payload.sub, payload.username)

        return tokens
