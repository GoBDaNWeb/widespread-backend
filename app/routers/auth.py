from fastapi import APIRouter, Cookie, Depends, Response

from app.dependencies.services import get_auth_service
from app.schemas.user import UserCredentials, UserFromDB

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register", response_model=UserFromDB)
async def register(
    user_credentials: UserCredentials,
    service=Depends(get_auth_service),
):
    return await service.register(user_credentials)


@auth_router.post("/login")
async def login(
    user_credentials: UserCredentials,
    response: Response,
    service=Depends(get_auth_service),
):
    return await service.login(response, user_credentials)


@auth_router.post("/logout")
async def logout(
    response: Response,
    refresh_token: str = Cookie(default=None),
    service=Depends(get_auth_service),
):
    return await service.logout(response, refresh_token)


@auth_router.post("/refresh_token")
async def refresh_token(
    response: Response,
    refresh_token: str = Cookie(default=None),
    service=Depends(get_auth_service),
):
    return await service.refresh_token(response, refresh_token)
