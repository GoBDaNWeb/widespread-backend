from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth import auth_router
from app.routers.user import user_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(user_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Разрешаем все домены (для тестирования)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
