import shutil

from fastapi import APIRouter, UploadFile

from tasks.tasks import process_picture

router = APIRouter(
    prefix="/images",
    tags=["Загрузка картинок"]
)

@router.post("/hotels")
async def add_hotel_image(name: int, file: UploadFile):
    image_path = f"static/images/{name}.webp"
    with open(image_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    process_picture.delay(image_path)

@router.post("/rooms")
async def add_room_image(name: int, file: UploadFile):
    with open(f"static/images/{name}.webp", "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

