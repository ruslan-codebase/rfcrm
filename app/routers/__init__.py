from fastapi import APIRouter
from .company_router import router as company_router


api_router = APIRouter()
api_router.include_router(company_router, prefix="/companies", tags=["company"])
