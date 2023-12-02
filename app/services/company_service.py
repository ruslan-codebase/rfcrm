from fastapi import HTTPException
from sqlalchemy import select
from uuid6 import UUID

from app.models.company import Company, CompanyIn, CompanyUpdate
from app.services.crud_service import CRUDService


class CompanyService(CRUDService):
    async def get(self, logged_in_email: str, offset: int = 0, limit: int = 20):
        result = await self.session.execute(
            select(Company)
            .where(Company.created_by == logged_in_email)
            .offset(offset)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_id(self, id: UUID, logged_in_email: str):
        company = await self.session.get(Company, id)
        if company is None:
            raise HTTPException(
                status_code=404, detail="Company not found with given id"
            )
        if company.created_by != logged_in_email:
            raise HTTPException(
                status_code=401,
                detail="Unauthorized",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return company

    async def create(self, model_in: CompanyIn, logged_in_email: str):
        company = Company(
            name=model_in.name,
            hh_employer_id=model_in.hh_employer_id,
            created_by=logged_in_email,
        )
        self.session.add(company)
        await self.session.commit()
        await self.session.refresh(company)
        return company

    async def delete(self, id: UUID, logged_in_email: str):
        company = await self.session.get(Company, id)
        if company is None:
            raise HTTPException(
                status_code=404, detail="Company not found with given id"
            )
        if company.created_by != logged_in_email:
            raise HTTPException(
                status_code=401,
                detail="Unauthorized",
                headers={"WWW-Authenticate": "Bearer"},
            )
        await self.session.delete(company)
        await self.session.commit()
        return id

    async def update(self, id: UUID, logged_in_email: str, model_in: CompanyUpdate):
        company = await self.session.get(Company, id)
        if company is None:
            raise HTTPException(
                status_code=404, detail="Company not found with given id"
            )
        if company.created_by != logged_in_email:
            raise HTTPException(
                status_code=401,
                detail="Unauthorized",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if model_in.name is not None:
            company.name = model_in.name
        if model_in.hh_employer_id is not None:
            company.hh_employer_id = model_in.hh_employer_id
        self.session.add(company)
        await self.session.commit()
        await self.session.refresh(company)
        return company
