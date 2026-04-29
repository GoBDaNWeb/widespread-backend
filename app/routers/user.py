from fastapi import APIRouter, Cookie, Depends

from app.dependencies.services import get_user_service

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.get("/me")
async def me(access_token: str = Cookie(default=None), service=Depends(get_user_service)):
    return await service.get_current_user(access_token)
