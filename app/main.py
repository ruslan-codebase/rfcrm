import uvicorn
from fastapi import FastAPI
from app.db import db
from app.routers import api_router

app = FastAPI(
    title="RFCRM",
    version="0.1.0",
)


@app.get("/")
async def api_root():
    return {"message": "Welcome to RFCRM"}


app.include_router(api_router, prefix="/api", tags=["api"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
