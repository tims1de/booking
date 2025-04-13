from celery import Celery
from celery.schedules import crontab

from config import settings

celery = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=["tasks.tasks",
             "tasks.scheduled"],
)

celery.conf.timezone = 'Europe/Moscow'


celery.conf.beat_schedule = {
    "taska_1": {
        "task": "periodic_task_1",
        "schedule": crontab(hour="9", minute="0")
    },
    "taska_2": {
        "task": "periodic_task_2",
        "schedule": crontab(hour="15", minute="30")
    }
}

