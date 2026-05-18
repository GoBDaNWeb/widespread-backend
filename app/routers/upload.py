from fastapi import APIRouter, UploadFile, File
from app.services.upload_service import save_upload

upload_router = APIRouter(prefix="/upload", tags=["Upload"])


@upload_router.post("/", summary="Загрузить изображение")
async def upload_image(file: UploadFile = File(...)) -> dict:
    """
    Принимает файл, сохраняет в media/, возвращает URL.
    Этот URL передаёшь в POST /images при создании ProductImage.
    """
    url = await save_upload(file)
    return {"url": url}