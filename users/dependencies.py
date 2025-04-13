from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, Request
from jose import JWTError, jwt

from config import settings
from exceptions import (
    IncorrectInformationUserException,
    IncorrectTokenFormatException,
    TokenExpiredException,
    TokenMissingException,
)
from users.dao import UsersDao


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenMissingException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.secret_key, settings.algorithm)
    except JWTError:
        raise IncorrectTokenFormatException
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise IncorrectInformationUserException
    user = await UsersDao.find_by_id(int(user_id))
    if not user:
        raise IncorrectInformationUserException

    return user
