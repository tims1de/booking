from datetime import date

from sqlalchemy import and_, func, or_
from sqlalchemy.future import select

from bookings.models import Bookings
from dao.base import BaseDao
from database import async_session_maker
from hotels.rooms.models import Rooms


def generate_booked_rooms_cte(date_from: date, date_to: date):
    return (
        select(
            Bookings.room_id,
            func.count(Bookings.room_id).label("count_of_booked_rooms"),
        )
        .where(
            or_(
                and_(Bookings.date_from >= date_from, Bookings.date_from <= date_to),
                and_(Bookings.date_from <= date_from, Bookings.date_to > date_from),
            ),
        )
        .group_by(Bookings.room_id)
        .cte("booked_rooms")
    )


async def func_for_get_num_of_left_rooms_group_by(
    date_from: date, date_to: date, hotel_id: int
):
    async with async_session_maker() as session:
        booked_rooms = generate_booked_rooms_cte(date_from, date_to)

        left_rooms = (
            select(
                Rooms.id,
                (
                    Rooms.quantity
                    - func.coalesce(booked_rooms.c.count_of_booked_rooms, 0)
                ).label("left_rooms"),
                # Свободные комнаты
            )
            .select_from(Rooms)
            .outerjoin(booked_rooms, Rooms.id == booked_rooms.c.room_id)
            .where(Rooms.hotel_id == hotel_id)
        )

        result = await session.execute(left_rooms)
        return result.mappings().all()


async def func_for_get_num_of_left_rooms_in_hotel(
    date_from: date, date_to: date, hotel_id: int
):
    async with async_session_maker() as session:
        booked_rooms = generate_booked_rooms_cte(date_from, date_to)

        free_rooms = (
            select(
                func.sum(
                    Rooms.quantity
                    - func.coalesce(booked_rooms.c.count_of_booked_rooms, 0)
                ).label("left_rooms")
            )
            .select_from(Rooms)
            .join(
                booked_rooms, Rooms.id == booked_rooms.c.room_id, isouter=True
            )  # Внешнее соединение
            .where(Rooms.hotel_id == hotel_id)
        )

        result = await session.execute(free_rooms)
        return result.scalar_one_or_none()


class RoomDao(BaseDao):
    model = Rooms

    @classmethod
    async def get_list_of_rooms_in_hotel(
        cls, date_from: date, date_to: date, hotel_id: int
    ):
        async with async_session_maker() as session:
            booked_rooms = generate_booked_rooms_cte(date_from, date_to)

            result_query = (
                select(
                    Rooms.id,
                    Rooms.hotel_id,
                    Rooms.name,
                    Rooms.description,
                    Rooms.services,
                    Rooms.price,
                    Rooms.quantity,
                    Rooms.image_id,
                    (Rooms.price * (date_to - date_from).days).label("total_cost"),
                    (
                        Rooms.quantity
                        - func.coalesce(booked_rooms.c.count_of_booked_rooms, 0)
                    ).label("left_rooms"),
                )
                .outerjoin(booked_rooms, Rooms.id == booked_rooms.c.room_id)
                .where(Rooms.hotel_id == hotel_id)
                .group_by(Rooms.id, booked_rooms.c.count_of_booked_rooms)
            )

            result = await session.execute(result_query)
            return result.mappings().all()
