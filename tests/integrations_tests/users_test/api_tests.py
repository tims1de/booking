import pytest
from httpx import AsyncClient

from tests.conftest import ac


@pytest.mark.parametrize("email, password, status_code", [
    ("Tima1234@dfsa.ru", "Tima", 200),
    ("Sharik@mail.ru", "Vladik", 200),
    ("test@test.com", "test", 409)
])
async def test_register_user(email, password, status_code,  ac: AsyncClient):
    response = await ac.post("/v1/auth/register", json={
        "email": email,
        "password": password
    })
    assert response.status_code == status_code


@pytest.mark.parametrize("email, password, status_code", [
    ("Tima1234@dfsa.ru", "Tima", 401),
    ("test@test.com", "test", 200),
    ("Vlad@qwer.com", "qwer", 401)
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/v1/auth/login", json={
        "email": email,
        "password": password
    })
    assert response.status_code == status_code



