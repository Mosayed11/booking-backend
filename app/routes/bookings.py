from fastapi import APIRouter, HTTPException, status, Depends
from datetime import date
from app.routes.auth import get_current_user
from app.schemas.booking import BookingCreate, BookingResponse

router = APIRouter(prefix='/bookings', tags=['bookings'])

bookings_db = {}
booking_counter = 1

@router.post('/', response_model=BookingResponse)
async def create_booking(booking_data: BookingCreate, current_user: str = Depends(get_current_user)):
    global booking_counter
    
    nights = (booking_data.check_out - booking_data.check_in).days
    total_price = nights * 100
    
    booking = {
        'id': booking_counter,
        'user_email': current_user,
        'room_id': booking_data.room_id,
        'check_in': booking_data.check_in,
        'check_out': booking_data.check_out,
        'guests': booking_data.guests,
        'total_price': total_price,
        'status': 'pending',
        'payment_status': 'unpaid',
        'payment_method': None,
        'created_at': date.today()
    }
    
    bookings_db[booking_counter] = booking
    booking_counter += 1
    
    return booking

@router.post('/{booking_id}/pay')
async def pay_booking(booking_id: int, payment_method: str, current_user: str = Depends(get_current_user)):
    booking = bookings_db.get(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail='Booking not found')
    if booking['user_email'] != current_user:
        raise HTTPException(status_code=403, detail='Not authorized')
    
    booking['payment_status'] = 'paid'
    booking['payment_method'] = payment_method
    booking['status'] = 'confirmed'
    
    return {'message': 'Payment successful', 'booking_id': booking_id}

@router.get('/', response_model=list[BookingResponse])
async def get_user_bookings(current_user: str = Depends(get_current_user)):
    user_bookings = [booking for booking in bookings_db.values() if booking['user_email'] == current_user]
    return user_bookings

@router.get('/{booking_id}', response_model=BookingResponse)
async def get_booking(booking_id: int, current_user: str = Depends(get_current_user)):
    booking = bookings_db.get(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail='Booking not found')
    if booking['user_email'] != current_user:
        raise HTTPException(status_code=403, detail='Not authorized')
    return booking

@router.delete('/{booking_id}')
async def cancel_booking(booking_id: int, current_user: str = Depends(get_current_user)):
    booking = bookings_db.get(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail='Booking not found')
    if booking['user_email'] != current_user:
        raise HTTPException(status_code=403, detail='Not authorized')
    
    booking['status'] = 'cancelled'
    return {'message': 'Booking cancelled'}
