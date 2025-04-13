from datetime import UTC, datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from config import settings
from users.dao import UsersDao

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()  # копируем входные данные
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=30
    )  # задаем время жизни токена
    to_encode.update({"exp": expire})  # добавляем к данным время жизни токена
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, settings.algorithm)
    # кодируем данные в токен
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDao.find_one_or_none(email=email)
    if not (user and verify_password(password, user.hashed_password)):
        return None
    return user
