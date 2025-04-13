import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from config import settings
from tasks.celery_app import celery
from tasks.email_templates import create_booking_confirmation_template


@celery.task
def process_picture(path: str):
    im_path = Path(path)
    im = Image.open(im_path)
    big_image = im.resize((1000, 500))
    small_image = im.resize((200, 100))

    big_image.save(f"static/images/big_image_1000_500_{im_path.name}")
    small_image.save(f"static/images/small_image_200_100_{im_path.name}")


@celery.task()
def send_booking_message(booking: dict, email_to: EmailStr):
    msg_content = create_booking_confirmation_template(booking, email_to)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
