from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.bookings import router as bookings_router
from app.routes.payments import router as payments_router
from app.routes.payments import router as payments_router
from app.db import Base, engine
import asyncio

app = FastAPI(title='Booking System Backend')

app.include_router(auth_router)
app.include_router(bookings_router)
app.include_router(payments_router)

@app.on_event('startup')
async def on_startup():
    pass

@app.get('/healthz')
async def health_check():
    return {'status': 'ok'}
