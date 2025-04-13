import pytest
from httpx import AsyncClient

# Endpoint для получения отелей (API-тест)
@pytest.mark.parametrize("date_from, date_to, status_code", [
    ("2023-10-01", "2023-09-01", 400),
    ("2023-07-10", "2023-09-01", 400),
    ("2023-06-16", "2023-06-17", 200)
])
async def test_add_booking_valid_date(date_from, date_to, status_code, authenticated_ac: AsyncClient):
    response = await authenticated_ac.post("/v1/bookings/add_booking", params={
        "room_id": 5,
        "date_from": date_from,
        "date_to": date_to,
    })

    assert response.status_code == status_code

# Получение и удаление бронирований (API-интеграционный-тест)
async def test_get_and_del_bookings(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/v1/bookings/by_user")
    assert response is not None
    assert response.status_code == 200

    bookings = response.json()

    for booking in bookings:
        booking_id = booking["id"]
        delete_response = await authenticated_ac.delete(f"/v1/bookings/{booking_id}")
        assert delete_response.status_code == 200

    response = await authenticated_ac.get("/v1/bookings/by_user")
    assert response.status_code == 409