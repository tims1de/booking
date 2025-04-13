from datetime import date, timedelta
from email.message import EmailMessage

from pydantic import EmailStr

from config import settings


def create_booking_confirmation_template(booking: dict, email_to: EmailStr):
    email = EmailMessage()

    email["Subject"] = "Подтверждение бронирования"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
        <h1>Подтвердите бронирование!</h1>
        <h3>Вы забронировали отель с {booking['date_from']} по {booking['date_to']}</h3>
        <h4>Комната типа - {booking['room_id']} </h4>
        <h4>Итоговая цена - {booking['total_cost']} BYN </h4>
        """,
        subtype='html'
    )

    return email

def date_plus_timedelta(days_plus: int):
    result_date = date.today() + timedelta(days=days_plus)
    return result_date

def create_remind_confirmation_template_date(booking: dict, booking_date_from: date, email_to: EmailStr):
    email = EmailMessage()

    if booking_date_from == date_plus_timedelta(1):
        email["Subject"] = "Завтра заселение!"
    elif booking_date_from == date_plus_timedelta(3):
        email["Subject"] = "Осталось 3 дня до заселения!"

    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>Напоминание о бронировании!</h1>
            <h3>Вы забронировали отель с {booking['date_from']} по {booking['date_to']}</h3>
            """,
        subtype='html'
    )

    return email
