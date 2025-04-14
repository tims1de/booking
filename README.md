# Cервис My_booking

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/-FastAPI-464646?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Alembic](https://img.shields.io/badge/-Alembic-464646?style=flat-square&logo=Alembic)](https://alembic.sqlalchemy.org/en/latest/)
[![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-464646?style=flat-square&logo=SQLAlchemy)](https://www.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Redis](https://img.shields.io/badge/-Redis-464646?style=flat-square&logo=Redis)](https://redis.io/)
[![Celery](https://img.shields.io/badge/-Celery-464646?style=flat-square&logo=Celery)](https://docs.celeryq.dev/en/stable/)
[![Sentry](https://img.shields.io/badge/-Sentry-464646?style=flat-square&logo=Sentry)](https://sentry.io/welcome/)
[![Prometheus](https://img.shields.io/badge/-Prometheus-464646?style=flat-square&logo=Prometheus)](https://prometheus.io/)
[![Grafana](https://img.shields.io/badge/-Grafana-464646?style=flat-square&logo=Grafana)](https://grafana.com/)
[![Uvicorn](https://img.shields.io/badge/-Uvicorn-464646?style=flat-square&logo=uvicorn)](https://www.uvicorn.org/)
[![Gunicorn](https://img.shields.io/badge/-Gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)

## Описание

Сервис для бронирования отелей позволяет пользователям резервировать различные типы номеров в отелях на заданные даты. Реализована функция загрузки изображений отелей. Пользователи могут просматривать доступные отели по местоположению на обычной странице. В системе предусмотрены логирование, мониторинг ошибок, сбор метрик и их визуализация. Проект использует асинхронный подход к обработке запросов и поддерживает локальное развертывание, а также развертывание в Docker-контейнерах.

### Регистрация и аутентификация

- Пользовательская система регистрации
- Неавторизованные пользователи имеют доступ только для чтения
- Аутентификация через куки и JWT-токены
- Создание новых записей разрешено только авторизованным пользователям
- Просмотр персональной информации в профиле

### Бронирование и управление

- Бронирование номеров в отелях
- Просмотр и отмена своих бронирований
- Отправка email-подтверждения через Celery

### Поиск и просмотр отелей

- Фильтрация отелей по местоположению и датам
- Отображение доступных отелей на странице
- Загрузка и обработка изображений отелей с помощью Celery

### Администрирование и инфраструктура

- Управление сервисом через админ-панель
- Кеширование и обработка фоновых задач через Redis
- Версионирование API
- Мониторинг ошибок через Sentry
- Кастомная система логирования
- Сбор метрик с Prometheus и визуализация в Grafana
- Развертывание в Docker

#### Локально документация доступна по адресу: <http://localhost:8000/v1/docs/>

#### Локальный запуск проекта

- Предварительно необходимо установить Docker и Redis для вашей системы.

- Склонировать репозиторий:

```bash
   git clone <название репозитория>
```

Cоздать и активировать виртуальное окружение:

Команды для установки виртуального окружения на Mac или Linux:

```bash
   python3 -m venv env
   source env/bin/activate
```

Команды для Windows:

```bash
   python -m venv venv
   source venv/Scripts/activate
```

- Перейти в директорию app:

```bash
   cd /app
```

- Создать файл .env по образцу:

```bash
   cp .env-non-dev .env
```

- Установить зависимости из файла requirements.txt:

```bash
   cd ..
   pip install -r requirements.txt
```

- Для создания миграций выполнить команду:

```bash
   alembic init migrations
```

- В папку migrations в env файл вставьте следующий код:

```bash
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.bookings.models import Booking
from app.config import settings
from app.database.db import Base
from app.hotels.models import Hotel
from app.rooms.models import Room
from app.users.models import User


config = context.config
config.set_main_option('sqlalchemy.url', f'{settings.DATABASE_URL}?async_fallback=True')

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata
```

- Инициализировать БД:

``` bash
    alembic revision --autogenerate -m "comment"  
```

- Применить миграцию:

``` bash
    alembic upgrade head 
```

- Запустить проект:

``` bash
    uvicorn app.main:app --reload   
```

- Запустить Redis:

``` bash
    redis-server.exe
    redis-cli.exe
```

- Запустить Celery:

``` bash
    celery -A app.tasks.celery:celery worker --loglevel=INFO --pool=solo
```

- Запустить Flower:

``` bash
    celery -A app.tasks.tasks:celery flower
```

#### Автор

Куприянов Тимофей - [https://github.com/tims1de](https://github.com/tims1de)
