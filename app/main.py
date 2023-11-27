import uvicorn
from fastapi import FastAPI
from app.db import db

app = FastAPI(
    title = "RFCRM",
    version = "0.1.0",
)

app.on_event("startup")
async def on_startup():
    await db.init_db()

@app.get("/")
async def api_root():
    return {"message": "Welcome to RFCRM"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)