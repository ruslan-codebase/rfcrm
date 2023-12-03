from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import db
from app.services.auth import oauth2_scheme
from app.services.company_service import CompanyService
from app.services.hh_service import HHService
from app.services.user_service import UserService

router = APIRouter()


@router.get("/update-companies", status_code=202)
async def update_companies(
    session: AsyncSession = Depends(db.get_session), token: str = Depends(oauth2_scheme)
):
    user = await UserService(session).get_logged_in_user(token)
    company_service = CompanyService(session)
    await HHService(session, company_service).create_companies_from_vacancy_search(
        user.email, text="python"
    )
