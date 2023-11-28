from fastapi import APIRouter, Depends, HTTPException
from uuid6 import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import db
from app.services.contact_service import ContactService
from app.models.contact import ContactIn, ContactUpdate, Contact


router = APIRouter()


@router.get("/", status_code=200)
async def get_contacts(session: AsyncSession = Depends(db.get_session)) -> list[Contact]:
    contacts = await ContactService(session).get()
    return contacts


@router.get("/{contact_id}", status_code=200)
async def get_contact_by_id(
    contact_id: UUID,
    session: AsyncSession = Depends(db.get_session)) -> Contact:
    
    contact = await ContactService(session).get_by_id(contact_id)

    if contact is None:
        raise HTTPException(
            status_code = 404,
            detail = "Contact not found with given id"
        )
    
    return contact


@router.post("/", status_code=201)
async def add_contact(
    contact_in: ContactIn,
    session: AsyncSession = Depends(db.get_session)) -> Contact:
    
    contact = await ContactService(session).create(contact_in)

    if contact is None:
        raise HTTPException(
            status_code = 404,
            detail = "Company not found with given id"
        )
    
    return contact


@router.put("/{contact_id}")
async def update_contact(
    contact_id: UUID,
    contact_update: ContactUpdate,
    session: AsyncSession = Depends(db.get_session)) -> Contact:

    contact = await ContactService(session).update(
        contact_id,
        contact_update
    )

    if contact is None:
        raise HTTPException(
            status_code = 404,
            detail = "Contact not found with given id"
        )
    
    return contact


@router.delete("/{contact_id}")
async def delete_contact(contact_id: UUID, session: AsyncSession = Depends(db.get_session)):
    cid = await ContactService(session).delete(contact_id)

    if cid is None:
        raise HTTPException(
            status_code = 404,
            detail = "Contact not found with given id"
        )
    
    return {"message": "successfully deleted"}