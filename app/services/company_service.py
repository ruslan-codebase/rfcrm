from uuid6 import UUID
from sqlalchemy import select
from app.services.crud_service import CRUDService
from app.models.company import Company, CompanyIn, CompanyUpdate


class CompanyService(CRUDService):
    async def get(self, offset: int = 0, limit: int = 20):
        result = await self.session.execute(select(Company).offset(offset).limit(limit))
        return result.scalars().all()

    async def get_by_id(self, id: UUID):
        company = await self.session.get(Company, id)
        return company

    async def create(self, model_in: CompanyIn):
        company = Company.from_orm(model_in)
        self.session.add(company)
        await self.session.commit()
        await self.session.refresh(company)
        return company

    async def delete(self, id: UUID):
        company = await self.session.get(Company, id)
        if company is None:
            return
        await self.session.delete(company)
        await self.session.commit()
        return id

    async def update(self, id: UUID, model_in: CompanyUpdate):
        company = await self.session.get(Company, id)
        if company is None:
            return
        if model_in.name is not None:
            company.name = model_in.name
        if model_in.hh_employer_id is not None:
            company.hh_employer_id = model_in.hh_employer_id
        self.session.add(company)
        await self.session.commit()
        await self.session.refresh(company)
        return company
