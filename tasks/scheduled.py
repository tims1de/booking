import asyncio
import smtplib

from bookings.dao import BookingDAO
from config import settings
from tasks.celery_app import celery
from tasks.email_templates import create_remind_confirmation_template_date


@celery.task(name="periodic_task_1")
def periodic_task_1():
    print("Задача запущена!")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_reminder_emails_tomorrow())
async def send_reminder_emails_tomorrow():
    bookings = await BookingDAO.get_bookings_date_from_input_date(1)
    if bookings:
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASS)
            for booking in bookings:
                msg = create_remind_confirmation_template_date(booking, booking.date_from, booking.email)
                server.send_message(msg)
                print(f"Сообщение для {booking.email} успешно доставлено!")


@celery.task(name="periodic_task_2")
def periodic_task_2():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_reminder_emails_3_days())
async def send_reminder_emails_3_days():
    bookings = await BookingDAO.get_bookings_date_from_input_date(3)
    if bookings:
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASS)
            for booking in bookings:
                msg = create_remind_confirmation_template_date(booking, booking.date_from, booking.email)
                server.send_message(msg)
                print(f"Сообщение для {booking.email} успешно доставлено!")
