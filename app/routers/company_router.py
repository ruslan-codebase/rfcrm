from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid6 import UUID

from app.db import db
from app.models.company import CompanyIn, CompanyOut, CompanyUpdate
from app.services.auth import oauth2_scheme
from app.services.company_service import CompanyService
from app.services.user_service import UserService

router = APIRouter()


@router.get("/", status_code=200)
async def get_companies(
    session: AsyncSession = Depends(db.get_session), token: str = Depends(oauth2_scheme)
) -> list[CompanyOut]:
    user = await UserService(session).get_logged_in_user(token)
    companies = await CompanyService(session).get(user.email)
    return [CompanyOut.from_company(c) for c in companies]


@router.get("/{company_id}", status_code=200)
async def get_company_by_id(
    company_id: UUID,
    session: AsyncSession = Depends(db.get_session),
    token: str = Depends(oauth2_scheme),
) -> CompanyOut:
    user = await UserService(session).get_logged_in_user(token)
    company = await CompanyService(session).get_by_id(company_id, user.email)
    return CompanyOut.from_company(company)


@router.post("/", status_code=201)
async def add_company(
    company_in: CompanyIn,
    session: AsyncSession = Depends(db.get_session),
    token: str = Depends(oauth2_scheme),
) -> CompanyOut:
    user = await UserService(session).get_logged_in_user(token)
    company = await CompanyService(session).create(company_in, user.email)
    return CompanyOut.from_company(company)


@router.put("/{company_id}", status_code=200)
async def update_company(
    company_id: UUID,
    company_update: CompanyUpdate,
    session: AsyncSession = Depends(db.get_session),
    token: str = Depends(oauth2_scheme),
) -> CompanyOut:
    user = await UserService(session).get_logged_in_user(token)
    company = await CompanyService(session).update(
        company_id, user.email, company_update
    )
    return CompanyOut.from_company(company)


@router.delete("/{company_id}", status_code=204)
async def delete_company(
    company_id: UUID,
    session: AsyncSession = Depends(db.get_session),
    token: str = Depends(oauth2_scheme),
):
    user = await UserService(session).get_logged_in_user(token)
    _ = await CompanyService(session).delete(company_id, user.email)
