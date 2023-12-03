from fastapi import APIRouter

from .company_router import router as company_router
from .contact_router import router as contact_router
from .hh_router import router as hh_router
from .user_router import router as user_router

api_router = APIRouter()
api_router.include_router(company_router, prefix="/companies", tags=["company"])
api_router.include_router(contact_router, prefix="/contacts", tags=["contact"])
api_router.include_router(user_router, prefix="/users", tags=["user"])
api_router.include_router(hh_router, prefix="/hh", tags=["hh"])
