import pytest

from users.dao import UsersDao


@pytest.mark.parametrize("email, is_exist, user_id", [
    ("test@test.com", True, 1),
    ("artem@example.com", True, 2),
    ("Tima@1234.com", False, 5)
])
async def test_find_user_by_id(email, is_exist, user_id):
    user = await UsersDao.find_by_id(user_id)

    if is_exist:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user
