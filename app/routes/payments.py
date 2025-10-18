from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from app.routes.auth import get_current_user

router = APIRouter(prefix='/payments', tags=['payments'])

payments_db = {}
payment_counter = 1

@router.post('/')
async def create_payment(booking_id: int, payment_method: str, current_user: str = Depends(get_current_user)):
    global payment_counter
    
    payment = {
        'id': payment_counter,
        'booking_id': booking_id,
        'payment_method': payment_method,
        'amount': 500.0,
        'status': 'completed',
        'created_at': datetime.now()
    }
    
    payments_db[payment_counter] = payment
    payment_counter += 1
    
    return payment

@router.get('/')
async def get_user_payments(current_user: str = Depends(get_current_user)):
    return list(payments_db.values())

@router.get('/{payment_id}')
async def get_payment(payment_id: int, current_user: str = Depends(get_current_user)):
    payment = payments_db.get(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail='Payment not found')
    return payment
