from fastapi import APIRouter, Depends

from app.core.security import oauth2_scheme
from app.dependencies.services import get_user_service

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.get("/me")
async def me(token: str = Depends(oauth2_scheme), service=Depends(get_user_service)):
    return await service.get_current_user(token)
