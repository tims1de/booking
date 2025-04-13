from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi_cache.decorator import cache

from hotels.rooms.router import get_list_of_rooms_of_a_specific_hotel
from hotels.router import get_hotels_by_location_and_date

router = APIRouter(
    prefix="/pages",
    tags=["Frontend"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/hotels")
async def get_hotels_page(request: Request, hotels=Depends(get_hotels_by_location_and_date)):
    return templates.TemplateResponse(
        name="hotels.html",
        context={"request": request, "hotels": hotels}
    )


@router.get("/search")
async def get_search_page(request: Request):
    return templates.TemplateResponse(
        name="search.html",
        context={"request": request}
    )

@router.get("/rooms_of_specific_hotel")
async def get_rooms_page(request: Request, rooms=Depends(get_list_of_rooms_of_a_specific_hotel)):
    return templates.TemplateResponse(
        name="rooms.html",
        context={"request": request, "rooms": rooms}
    )


