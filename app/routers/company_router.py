from fastapi import APIRouter, Depends, HTTPException
from uuid6 import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import db
from app.services.company_service import CompanyService
from app.models.company import CompanyIn, CompanyUpdate

router = APIRouter()


@router.get("/")
async def get_companies(session: AsyncSession = Depends(db.get_session)):
    companies = await CompanyService(session).get()
    return {"data": companies, "message": ""}


@router.get("/{company_id}")
async def get_company_by_id(
    company_id: UUID, session: AsyncSession = Depends(db.get_session)
):
    company = await CompanyService(session).get_by_id(company_id)

    if company is None:
        raise HTTPException(status_code=404, detail="Company not found with given id")

    return {"data": company, "message": ""}


@router.post("/")
async def add_company(
    company_in: CompanyIn, session: AsyncSession = Depends(db.get_session)
):
    company = await CompanyService(session).create(company_in)
    return {"data": company, "message": ""}


@router.put("/{company_id}")
async def update_company(
    company_id: UUID,
    company_update: CompanyUpdate,
    session: AsyncSession = Depends(db.get_session),
):
    company = await CompanyService(session).update(company_id, company_update)

    if company is None:
        raise HTTPException(status_code=404, detail="Company not found with given id")

    return {"data": company, "message": ""}


@router.delete("/{company_id}")
async def delete_company(
    company_id: UUID, session: AsyncSession = Depends(db.get_session)
):
    cid = await CompanyService(session).delete(company_id)

    if cid is None:
        raise HTTPException(status_code=404, detail="Company not found with given id")

    return {"data": "", "message": "successfully deleted"}
