from fastapi import APIRouter, Depends, Response
from fastapi_versioning import version

from exceptions import IncorrectEmailOrPasswordException, UserAlreadyExistsException
from users.auth import authenticate_user, create_access_token, get_password_hash
from users.dao import UsersDao
from users.dependencies import get_current_user
from users.models import Users
from users.schemas import SUserAuth

router = APIRouter(prefix="/auth", tags=["Auth & Пользователи"])


@router.post("/register")
@version(1)
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDao.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDao.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
@version(1)
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token


@router.post("/logout")
@version(1)
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@router.get("/me")
@version(1)
async def read_user_me(current_user: Users = Depends(get_current_user)):
    return current_user
