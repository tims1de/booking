from datetime import date, timedelta

from sqlalchemy import and_, delete, func, insert, select
from sqlalchemy.sql.functions import coalesce

from bookings.models import Bookings
from dao.base import BaseDao
from database import async_session_maker
from exceptions import (
    IncorrectDate,
    IncorrectDateDays,
    RoomCannotBeBooked,
    UnknownBooking,
)
from hotels.rooms.dao import generate_booked_rooms_cte
from hotels.rooms.models import Rooms
from users.models import Users


def date_plus_timedelta(days_plus: int):
    result_date = date.today() + timedelta(days=days_plus)
    return result_date


class BookingDAO(BaseDao):
    model = Bookings

    @classmethod
    async def add(cls, user_id, room_id: int, date_from: date, date_to: date):
        async with async_session_maker() as session:

            if date_from >= date_to:
                raise IncorrectDate

            if date_to - date_from > timedelta(days=30):
                raise IncorrectDateDays

            booked_rooms = generate_booked_rooms_cte(date_from, date_to)

            get_rooms_left = (
                select(
                    (
                        Rooms.quantity
                        - coalesce(func.sum(booked_rooms.c.count_of_booked_rooms), 0)
                    ).label("rooms_left")
                )
                .select_from(Rooms)
                .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                .where(Rooms.id == room_id)
                .group_by(Rooms.quantity)
            )

            rooms_left = await session.execute(get_rooms_left)
            rooms_left = rooms_left.scalar()
            print(f"DEBUG: rooms_left = {rooms_left}")

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = (
                    insert(Bookings)
                    .values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    )
                    .returning(Bookings)
                )

                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()

            else:
                raise RoomCannotBeBooked

    @classmethod
    async def del_booking(cls, user_id: int, booking_id: int):
        async with async_session_maker() as session:
            query_id = select(Bookings.user_id).where(Bookings.id == booking_id)
            query_id_result = await session.execute(query_id)
            if query_id_result.scalar() != user_id:
                raise UnknownBooking

            query = delete(Bookings).where(
                and_(Bookings.id == booking_id, Bookings.user_id == user_id)
            )
            await session.execute(query)
            await session.commit()
            return "Бронь успешно удалена!"

    @classmethod
    async def get_users_bookings_info(cls, user_id: int):
        async with async_session_maker() as session:
            user_bookings = (
                select(
                    Bookings.room_id,
                    Bookings.user_id,
                    Bookings.date_from,
                    Bookings.date_to,
                    Bookings.price,
                    Bookings.total_cost,
                    Bookings.total_days,
                    Bookings.id,
                    Rooms.image_id,
                    Rooms.name,
                    Rooms.description,
                    Rooms.services,
                )
                .select_from(Bookings)
                .join(Rooms, Bookings.room_id == Rooms.id)
                .where(Bookings.user_id == user_id)
            )

            all_bookings = await session.execute(user_bookings)
            return all_bookings.mappings().all()

    @classmethod
    async def get_bookings_date_from_input_date(cls, input_date):
        final_date = date_plus_timedelta(input_date)
        async with async_session_maker() as session:
            users_bookings = (
                select(
                    Bookings.room_id,
                    Bookings.user_id,
                    Bookings.date_from,
                    Bookings.date_to,
                    Bookings.price,
                    Bookings.total_cost,
                    Bookings.total_days,
                    Bookings.id,
                    Users.email,
                )
                .select_from(Bookings)
                .join(Users, Bookings.user_id == Users.id)
                .where(Bookings.date_from == final_date)
            )

            all_bookings = await session.execute(users_bookings)
            return all_bookings.mappings().all()
