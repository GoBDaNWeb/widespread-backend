from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.routers.auth import auth_router
from app.routers.product import category_router, product_router, sizes_router, image_router, brand_router
from app.routers.upload import upload_router
from app.routers.user import user_router

MEDIA_ROOT = Path(__file__).resolve().parent.parent / "media"
MEDIA_ROOT.mkdir(exist_ok=True)


app = FastAPI()

app.mount("/media", StaticFiles(directory=MEDIA_ROOT), name="media")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(category_router)
app.include_router(brand_router)
app.include_router(sizes_router)
app.include_router(product_router)
app.include_router(image_router)
app.include_router(upload_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Разрешаем все домены (для тестирования)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
