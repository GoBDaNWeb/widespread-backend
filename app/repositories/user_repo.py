from abc import ABC, abstractmethod

from sqlalchemy import select

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCredentials


class UserRepository(ABC):
    @abstractmethod
    async def register(self, user_credentials: UserCredentials):
        pass

    @abstractmethod
    async def login(self, user_credentials: UserCredentials):
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int):
        pass


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session):
        self.session = session

    async def _get_user_by_credentials(self, user_credentials: UserCredentials):
        stmt = select(User).where(User.username == user_credentials.username)
        result = await self.session.execute(stmt)

        existing_user = result.scalar_one_or_none()
        return existing_user

    async def register(self, user_credentials: UserCredentials):
        existing_user = await self._get_user_by_credentials(user_credentials)

        if existing_user:
            return None

        new_user = user_credentials.model_dump()
        new_user["password"] = hash_password(user_credentials.password)
        new_user = User(**new_user)
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)

        return new_user

    async def login(self, user_credentials: UserCredentials):
        existing_user = await self._get_user_by_credentials(user_credentials)

        return existing_user

    async def get_user_by_id(self, user_id: int):
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        existing_user = result.scalar_one_or_none()

        return existing_user
