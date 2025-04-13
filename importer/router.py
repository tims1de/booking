import codecs
import csv
from typing import Literal

from fastapi import APIRouter, BackgroundTasks, Depends, UploadFile
from fastapi_versioning import version

from dao.base import BaseDao
from users.dependencies import get_current_user

router = APIRouter(
    prefix='/import',
    tags=['import']
)

@router.post('/{table_name}', dependencies=[Depends(get_current_user)],status_code=201)
@version(1)
async def import_csv(
    table_name: Literal["bookings", "rooms", "hotels", "users"],
    file: UploadFile,
    background_tasks: BackgroundTasks,
):
    csvReader = csv.DictReader(codecs.iterdecode(file.file, "utf-8"), delimiter=";")
    background_tasks.add_task(file.file.close)
    return await BaseDao.add_by_csv(table_name, csvReader)