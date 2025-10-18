from pydantic import BaseModel
from datetime import date, datetime

class BookingCreate(BaseModel):
    room_id: str
    check_in: date
    check_out: date
    guests: int = 1

class BookingResponse(BaseModel):
    id: int
    user_email: str
    room_id: str
    check_in: date
    check_out: date
    guests: int
    total_price: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
