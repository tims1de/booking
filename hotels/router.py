from datetime import date

from fastapi import APIRouter
from fastapi_cache.decorator import cache
from fastapi_versioning import version

from hotels.dao import HotelsDao
from hotels.shemas import SHotels_by_id, SHotels_by_location

router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get("/{location}", response_model=list[SHotels_by_location])
@version(1)
async def get_hotels_by_location_and_date(
    location: str, date_from: date, date_to: date
):
    return await HotelsDao.get_hotels_by_location_and_date(location, date_from, date_to)


@cache(expire=60)
@router.get("/id/{hotel_id}", response_model=list[SHotels_by_id])
@version(1)
async def get_hotels_by_id(hotel_id: int):
    return await HotelsDao.get_hotel(hotel_id)
