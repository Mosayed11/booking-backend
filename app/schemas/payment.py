from pydantic import BaseModel
from datetime import datetime

class PaymentCreate(BaseModel):
    booking_id: int
    payment_method: str
    amount: float

class PaymentResponse(BaseModel):
    id: int
    booking_id: int
    payment_method: str
    amount: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
