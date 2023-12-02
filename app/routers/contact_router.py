from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid6 import UUID

from app.db import db
from app.models.contact import ContactIn, ContactOut, ContactUpdate
from app.services.auth import oauth2_scheme
from app.services.contact_service import ContactService
from app.services.user_service import UserService

router = APIRouter()


@router.get("/", status_code=200)
async def get_contacts(
    session: AsyncSession = Depends(db.get_session), token: str = Depends(oauth2_scheme)
) -> list[ContactOut]:
    user = await UserService(session).get_logged_in_user(token)
    contacts = await ContactService(session).get(user.email)
    return [ContactOut.from_contact(c) for c in contacts]


@router.get("/{contact_id}", status_code=200)
async def get_contact_by_id(
    contact_id: UUID,
    session: AsyncSession = Depends(db.get_session),
    token: str = Depends(oauth2_scheme),
) -> ContactOut:
    user = await UserService(session).get_logged_in_user(token)
    contact = await ContactService(session).get_by_id(contact_id, user.email)
    return ContactOut.from_contact(contact)


@router.post("/", status_code=201)
async def add_contact(
    contact_in: ContactIn,
    session: AsyncSession = Depends(db.get_session),
    token: str = Depends(oauth2_scheme),
) -> ContactOut:
    user = await UserService(session).get_logged_in_user(token)
    contact = await ContactService(session).create(contact_in, user.email)
    return ContactOut.from_contact(contact)


@router.put("/{contact_id}", status_code=200)
async def update_contact(
    contact_id: UUID,
    contact_update: ContactUpdate,
    session: AsyncSession = Depends(db.get_session),
    token: str = Depends(oauth2_scheme),
) -> ContactOut:
    user = await UserService(session).get_logged_in_user(token)
    contact = await ContactService(session).update(
        contact_id, user.email, contact_update
    )
    return ContactOut.from_contact(contact)


@router.delete("/{contact_id}", status_code=204)
async def delete_contact(
    contact_id: UUID,
    session: AsyncSession = Depends(db.get_session),
    token: str = Depends(oauth2_scheme),
):
    user = await UserService(session).get_logged_in_user(token)
    _ = await ContactService(session).delete(contact_id, user.email)
