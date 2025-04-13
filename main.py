import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from urllib.request import Request

import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from redis import asyncio as aioredis
from sqladmin import Admin

from admin.auth import authentication_backend
from admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UserAdmin
from bookings.router import router as router_bookings
from config import settings
from database import engine
from hotels.rooms.router import router as router_rooms
from hotels.router import router as router_hotels
from images.router import router as router_images
from importer.router import router as router_import
from logger import logger
from pages.router import router as router_pages
from prometheus.router import router as router_prometheus
from users.models import Users
from users.router import router as router_users


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield

app = FastAPI(lifespan=lifespan)


sentry_sdk.init(
    dsn=f"{settings.DSN}",
    traces_sample_rate=1.0,
)

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_pages)
app.include_router(router_images)
app.include_router(router_import)
app.include_router(router_prometheus)

app = VersionedFastAPI(
    app,
    version_format='{major}',
    prefix_format='/v{major}',
)

instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*"],
)
instrumentator.instrument(app).expose(app)

app.mount("/static", StaticFiles(directory="static"), "static")

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UserAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(HotelsAdmin)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
