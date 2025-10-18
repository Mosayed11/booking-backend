from fastapi import FastAPI
from app.routes.auth import router as auth_router  # ✅ صحfrom app.db import Base, engine
import asyncio

app = FastAPI(title="Booking System Backend")

app.include_router(auth_router)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/healthz")
async def health_check():
    return {"status": "ok"}
