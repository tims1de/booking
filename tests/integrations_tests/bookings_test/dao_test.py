from datetime import datetime

from bookings.dao import BookingDAO


async def test_add_and_get_booking():
    booking = await BookingDAO.add(
        user_id=2,
        room_id=2,
        date_from=datetime.strptime("2025-06-16", "%Y-%m-%d"),
        date_to=datetime.strptime("2025-06-20", "%Y-%m-%d"),
    )

    # проверяем корректность данных
    assert booking.user_id == 2
    assert booking.room_id == 2

    # проверяем что в базу действительно добавилась новая бронь
    new_booking = await BookingDAO.find_by_id(booking.id)
    assert new_booking is not None

# Работа с бронированиями через БД (интеграционный тест)
async def test_add_read_and_del_booking():
    booking = await BookingDAO.add(
        user_id=2,
        room_id=2,
        date_from=datetime.strptime("2025-06-16", "%Y-%m-%d"),
        date_to=datetime.strptime("2025-06-20", "%Y-%m-%d"),
    )

    booking_id = booking.id
    assert booking_id is not None

    read_booking = await BookingDAO.find_by_id(booking_id)
    assert read_booking is not None
    assert read_booking.user_id == 2
    assert read_booking.room_id == 2

    delete_success = await BookingDAO.del_booking(user_id=2, booking_id=booking_id)
    assert delete_success is not None

    deleted_booking = await BookingDAO.find_by_id(booking_id)
    assert deleted_booking is None





