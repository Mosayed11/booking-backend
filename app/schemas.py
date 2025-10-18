from pydantic import BaseModel, condecimal
from datetime import date, datetime
import uuid

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str | None = None

class UserResponse(BaseModel):  # أضف هذا ال class
    id: int
    email: str
    full_name: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class PropertyCreate(BaseModel):
    title: str
    description: str | None = None
    address: str | None = None
    city: str | None = None
    country: str | None = None

class PropertyOut(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None = None
    city: str | None = None
    country: str | None = None

    class Config:
        from_attributes = True

class RoomCreate(BaseModel):
    property_id: uuid.UUID
    name: str
    capacity: int = 1
    price_per_night: condecimal(max_digits=10, decimal_places=2)

class RoomOut(BaseModel):
    id: uuid.UUID
    property_id: uuid.UUID
    name: str
    capacity: int
    price_per_night: condecimal(max_digits=10, decimal_places=2)

    class Config:
        from_attributes = True

class BookingCreate(BaseModel):
    room_id: uuid.UUID
    check_in: date
    check_out: date

class BookingOut(BaseModel):
    id: uuid.UUID
    room_id: uuid.UUID
    check_in: date
    check_out: date
    status: str
    total_price: condecimal(max_digits=10, decimal_places=2)

    class Config:
        from_attributes = True
