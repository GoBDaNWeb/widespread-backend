import uuid
from pathlib import Path

from fastapi import UploadFile

MEDIA_ROOT = Path(__file__).resolve().parent.parent.parent / "media"
MEDIA_ROOT.mkdir(exist_ok=True)

MEDIA_URL = "/media"

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_SIZE_MB = 5


async def save_upload(file: UploadFile) -> str:
    if file.content_type not in ALLOWED_TYPES:
        from fastapi import HTTPException, status
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Недопустимый тип файла: {file.content_type}. Разрешены: jpeg, png, webp, gif",
        )

    content = await file.read()

    if len(content) > MAX_SIZE_MB * 1024 * 1024:
        from fastapi import HTTPException, status
        raise HTTPException(
            status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Файл слишком большой. Максимум {MAX_SIZE_MB} MB",
        )

    suffix = Path(file.filename).suffix.lower()
    filename = f"{uuid.uuid4().hex}{suffix}"

    dest = MEDIA_ROOT / filename
    dest.write_bytes(content)

    return f"{MEDIA_URL}/{filename}"