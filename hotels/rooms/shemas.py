from pydantic import BaseModel, ConfigDict


class SRooms(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    services: list[str]
    price: int
    quantity: int
    image_id: int
    total_cost: int
    rooms_left: int

    model_config = ConfigDict(from_attributes=True)


class SGroup_by_left_rooms(BaseModel):
    id: int
    left_rooms: int

    model_config = ConfigDict(from_attributes=True)


class SList_rooms_of_specific_hotel(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    services: list[str]
    price: int
    quantity: int
    image_id: int
    total_cost: int
    left_rooms: int

    model_config = ConfigDict(from_attributes=True)
