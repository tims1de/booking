from dao.base import BaseDao
from users.models import Users


class UsersDao(BaseDao):
    model = Users
