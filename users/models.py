from passlib.context import CryptContext
from sqlalchemy import event
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(mapper, connection, target):
    if target.hashed_password:
        target.hashed_password = pwd_context.hash(target.hashed_password)


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    hashed_password: Mapped[str]

    booking = relationship("Bookings", back_populates="user")

    def __str__(self):
        return f"Пользователь: {self.email}"


event.listen(Users, "before_insert", hash_password)
event.listen(Users, "before_update", hash_password)
