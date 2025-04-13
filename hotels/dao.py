from datetime import date

from sqlalchemy import and_, func, select

from dao.base import BaseDao
from database import async_session_maker
from exceptions import UnknownHotel
from hotels.models import Hotels
from hotels.rooms.dao import generate_booked_rooms_cte
from hotels.rooms.models import Rooms


class HotelsDao(BaseDao):
    model = Hotels

    @classmethod
    async def get_hotels_by_location_and_date(
        cls, location: str, date_from: date, date_to: date
    ):
        async with async_session_maker() as session:
            booked_rooms = generate_booked_rooms_cte(date_from, date_to)

            booked_hotels = (
                select(
                    Rooms.hotel_id,
                    func.sum(
                        Rooms.quantity
                        - func.coalesce(booked_rooms.c.count_of_booked_rooms, 0)
                    ).label("rooms_left"),
                )
                .select_from(Rooms)
                .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                .group_by(Rooms.hotel_id)
                .cte("booked_hotels")
            )

            hotels_with_rooms = (
                select(
                    Hotels.id,
                    Hotels.name,
                    Hotels.location,
                    Hotels.services,
                    Hotels.rooms_quantity,
                    Hotels.image_id,
                    booked_hotels.c.rooms_left,
                )
                .join(
                    booked_hotels,
                    booked_hotels.c.hotel_id == Hotels.id,
                )
                .where(
                    and_(
                        booked_hotels.c.rooms_left > 0,
                        Hotels.location.like(f"%{location}%"),
                    )
                )
                .order_by(Hotels.id)
            )

            hotels_with_rooms = await session.execute(hotels_with_rooms)
            return hotels_with_rooms.mappings().all()

    @classmethod
    async def get_hotel(cls, hotel_id: int):
        async with async_session_maker() as session:
            hotel_query = select(
                Hotels.id,
                Hotels.name,
                Hotels.location,
                Hotels.services,
                Hotels.rooms_quantity,
                Hotels.image_id,
            ).where(Hotels.id == hotel_id)

            result = await session.execute(hotel_query)
            result_hotel = result.mappings().all()

            if result_hotel is None:
                raise UnknownHotel

            return result_hotel
