from abc import ABC, abstractmethod

from sqlalchemy import delete, select

from app.core.security import hash_token
from app.models.token import RefreshToken


class TokenRepository(ABC):
    @abstractmethod
    async def get_refresh_token(self, token: str):
        pass

    @abstractmethod
    async def save_refresh_token(self, user_id: int, token: str):
        pass

    @abstractmethod
    async def delete_refresh_token(self, token: str):
        pass


class SQLAlchemyTokenRepository(TokenRepository):
    def __init__(self, session):
        self.session = session

    async def get_refresh_token(self, token: str):
        stmt = select(RefreshToken).where(RefreshToken.token == hash_token(token))

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def save_refresh_token(self, user_id: int, token: str):
        refresh_token = RefreshToken(
            user_id=user_id,
            token=hash_token(token),
        )
        self.session.add(refresh_token)
        await self.session.commit()

    async def delete_refresh_token(self, token: str):
        stmt = delete(RefreshToken).where(RefreshToken.token == hash_token(token))
        await self.session.execute(stmt)
        await self.session.commit()
