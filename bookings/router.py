from datetime import date

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from fastapi_versioning import version

from bookings.dao import BookingDAO
from bookings.shemas import SBooking, SBookings_by_user
from exceptions import NotBooking, RoomCannotBeBooked
from tasks.tasks import send_booking_message
from users.dependencies import get_current_user
from users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("/all_bookings")
@version(1)
async def get_bookings():
    return await BookingDAO.find_all()

@cache(expire=60)
@router.get("/tomorrow_bookings")
@version(1)
async def get_bookings_tomorrow():
    return await BookingDAO.get_bookings_date_from_input_date(1)


@router.get("/3_days_bookings")
@version(1)
async def get_bookings_3_days():
    return await BookingDAO.get_bookings_date_from_input_date(3)

@cache(expire=60)
@router.get("/by_user", response_model=list[SBookings_by_user])
@version(1)
async def get_bookings_by_user(user: Users = Depends(get_current_user)):
    bookings_by_user = await BookingDAO.get_users_bookings_info(user_id=user.id)
    if not bookings_by_user:
        raise NotBooking
    return bookings_by_user


@router.post("/add_booking")
@version(1)
async def add_booking_for_user(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
):
    add_booking = await BookingDAO.add(
        user_id=user.id, room_id=room_id, date_from=date_from, date_to=date_to
    )
    if not add_booking:
        raise RoomCannotBeBooked
    booking_dict = SBooking.model_validate(add_booking).model_dump()
    send_booking_message.delay(booking_dict, user.email)
    return booking_dict


@router.delete("/{booking_id}")
@version(1)
async def del_booking_for_user(
    booking_id: int, user: Users = Depends(get_current_user)
):
    del_bookings = await BookingDAO.del_booking(user_id=user.id, booking_id=booking_id)
    return del_bookings
