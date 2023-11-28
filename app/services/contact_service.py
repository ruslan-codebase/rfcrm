from uuid6 import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.services.crud_service import CRUDService
from app.models.contact import Contact, ContactIn, ContactUpdate
from app.models.company import Company


class ContactService(CRUDService):

    async def get(self, offset:int = 0, limit:int = 20):
        result = await self.session.execute(
            select(Contact).offset(offset).limit(limit)
        )
        return result.scalars().all()
    
    async def get_by_id(self, id: UUID):
        contact = await self.session.get(Contact, id)
        return contact
    
    async def create(self, model_in: ContactIn):
        if model_in.company_id is not None:
            company = await self.session.get(Company, model_in.company_id)
            if company is None:
                return
        
        contact = Contact.from_orm(model_in)
        self.session.add(contact)
        await self.session.commit()
        await self.session.refresh(contact)
        return contact
    
    async def delete(self, id: UUID):
        contact = await self.session.get(Contact, id)
        if contact is None:
            return
        await self.session.delete(contact)
        await self.session.commit()
        return id
    
    async def update(self, id: UUID, model_in: ContactUpdate):
        contact = await self.session.get(Contact, id)
        if contact is None:
            return

        if model_in.company_id is not None:
            company = self.session.get(Company, model_in.company_id)
            if company is None:
                return
        
        for field, value in model_in.__dict__.items():
            if value is not None:
                if field == "company_id":
                    company = self.session.get(Company, value)
                    if company is None:
                        return
                setattr(contact, field, value)
        
        self.session.add(contact)
        await self.session.commit()
        await self.session.refresh(contact)
        return contact

