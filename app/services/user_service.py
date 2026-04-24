from fastapi import HTTPException

from app.core.security import decode_jwt
from app.repositories.user_repo import UserRepository
from app.schemas.token import TokenEnum
from app.schemas.user import UserFromDB


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get_current_user(self, token: str):
        payload = decode_jwt(token)

        if not payload or payload.type != TokenEnum.ACCESS_TOKEN:
            raise HTTPException(status_code=403, detail="Unauthorized")

        user = await self.user_repo.get_user_by_id(payload.sub)

        if not user:
            raise HTTPException(status_code=404, detail="User does not exist")

        response_user = UserFromDB.model_validate(user)

        return response_user
