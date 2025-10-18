from fastapi import FastAPI

app = FastAPI(title="Booking System Backend")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/healthz")
async def health_check():
    return {"status": "ok"}