from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.repositories.product_repo import SQLAlchemyProductRepository
from app.repositories.token_repo import SQLAlchemyTokenRepository
from app.repositories.user_repo import SQLAlchemyUserRepository


def get_user_repository(session: AsyncSession = Depends(get_async_session)):
    return SQLAlchemyUserRepository(session)


def get_token_repository(session: AsyncSession = Depends(get_async_session)):
    return SQLAlchemyTokenRepository(session)


def get_product_repository(session: AsyncSession = Depends(get_async_session)):
    return SQLAlchemyProductRepository(session)