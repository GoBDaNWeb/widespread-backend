from fastapi import Depends

from app.dependencies.repositories import get_token_repository, get_user_repository, get_product_repository
from app.repositories.product_repo import ProductRepository
from app.repositories.user_repo import UserRepository
from app.services.auth_service import AuthService
from app.services.product_service import ProductService
from app.services.user_service import UserService


async def get_auth_service(
    user_repo: AuthService = Depends(get_user_repository),
    token_repo: AuthService = Depends(get_token_repository),
):
    return AuthService(user_repo, token_repo)


async def get_user_service(user_repo: UserRepository = Depends(get_user_repository)):
    return UserService(user_repo)


async def get_product_service(product_repo: ProductRepository = Depends(get_product_repository)):
    return ProductService(product_repo)