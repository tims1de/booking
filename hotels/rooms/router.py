from datetime import date

from fastapi import APIRouter
from fastapi_cache.decorator import cache
from fastapi_versioning import version

from hotels.rooms.dao import (
    RoomDao,
    func_for_get_num_of_left_rooms_group_by,
    func_for_get_num_of_left_rooms_in_hotel,
)
from hotels.rooms.shemas import SGroup_by_left_rooms, SList_rooms_of_specific_hotel

router = APIRouter(
    tags=["Комнаты"],
)

@cache(expire=60)
@router.get("/left_rooms_of_{hotel_id}", response_model=int)
@version(1)
async def get_num_of_left_rooms_in_hotel(date_from: date, date_to: date, hotel_id: int):
    return await func_for_get_num_of_left_rooms_in_hotel(date_from, date_to, hotel_id)

@cache(expire=60)
@router.get(
    "/group_by_left_rooms_of_{hotel_id}", response_model=list[SGroup_by_left_rooms]
)
@version(1)
async def get_num_of_left_rooms_group_by(date_from: date, date_to: date, hotel_id: int):
    return await func_for_get_num_of_left_rooms_group_by(date_from, date_to, hotel_id)

@router.get(
    "/hotels/{hotel_id}/rooms", response_model=list[SList_rooms_of_specific_hotel]
)
@version(1)
async def get_list_of_rooms_of_a_specific_hotel(
    date_from: date, date_to: date, hotel_id: int
):
    return await RoomDao.get_list_of_rooms_in_hotel(date_from, date_to, hotel_id)
