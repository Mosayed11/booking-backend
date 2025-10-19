from fastapi import FastAPI
from app.routes import auth
from app.db import engine, Base
import logging

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Booking System API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}