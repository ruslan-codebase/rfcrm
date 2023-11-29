from fastapi import HTTPException
from sqlalchemy import select
from uuid6 import UUID

from app.models.company import Company
from app.models.contact import Contact, ContactIn, ContactUpdate
from app.services.crud_service import CRUDService


class ContactService(CRUDService):
    async def get(self, offset: int = 0, limit: int = 20):
        result = await self.session.execute(select(Contact).offset(offset).limit(limit))
        return result.scalars().all()

    async def get_by_id(self, id: UUID):
        contact = await self.session.get(Contact, id)
        if contact is None:
            raise HTTPException(
                status_code=404, detail="Contact not found with given id"
            )
        return contact

    async def create(self, model_in: ContactIn):
        if model_in.company_id is not None:
            company = await self.session.get(Company, model_in.company_id)
            if company is None:
                raise HTTPException(
                    status_code=404, detail="Company not found with given id"
                )

        contact = Contact.from_orm(model_in)
        self.session.add(contact)
        await self.session.commit()
        await self.session.refresh(contact)
        return contact

    async def delete(self, id: UUID):
        contact = await self.session.get(Contact, id)
        if contact is None:
            raise HTTPException(
                status_code=404, detail="Contact not found with given id"
            )
        await self.session.delete(contact)
        await self.session.commit()
        return id

    async def update(self, id: UUID, model_in: ContactUpdate):
        contact = await self.session.get(Contact, id)
        if contact is None:
            raise HTTPException(
                status_code=404, detail="Contact not found with given id"
            )

        if model_in.company_id is not None:
            company = self.session.get(Company, model_in.company_id)
            if company is None:
                raise HTTPException(
                    status_code=404, detail="Company not found with given id"
                )

        for field, value in model_in.__dict__.items():
            if value is not None:
                setattr(contact, field, value)

        self.session.add(contact)
        await self.session.commit()
        await self.session.refresh(contact)
        return contact
