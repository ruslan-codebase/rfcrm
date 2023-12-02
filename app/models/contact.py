from typing import Optional

from pydantic import validator
from sqlmodel import Field, SQLModel
from uuid6 import UUID

from app.models.base_model import BaseModel


class PhoneBase(SQLModel):
    phone_number: Optional[int]

    @validator("phone_number")
    def phone_validation(cls, v):
        if v is None:
            return

        str_v = str(v)

        if type(v) is not int:
            raise ValueError("Phone number is not an int")

        if not str_v.startswith("7"):
            raise ValueError("Phone number must start with 7")

        if len(str_v) != 11:
            # 1 digit country code
            # 3 digits region code
            # 7 digits phone number
            raise ValueError("Phone number must be 11 digits long.")

        return v


class CreatorBase(SQLModel):
    created_by: str


class ContactBase(SQLModel):
    firstname: str
    lastname: str
    patronymic: Optional[str]
    telegram_name: Optional[str]
    company_id: Optional[UUID] = Field(default=None, foreign_key="Company.id")


class Contact(BaseModel, CreatorBase, ContactBase, PhoneBase, table=True):
    pass


class ContactIn(ContactBase, PhoneBase):
    pass


class ContactUpdate(PhoneBase):
    firstname: Optional[str]
    lastname: Optional[str]
    patronymic: Optional[str]
    telegram_name: Optional[str]
    company_id: Optional[UUID]


class ContactOut(BaseModel, PhoneBase):
    firstname: str
    lastname: str
    patronymic: Optional[str]
    telegram_name: Optional[str]
    company_url: Optional[str]

    @staticmethod
    def from_contact(contact: Contact):
        return ContactOut(
            id=contact.id,
            created_at=contact.created_at,
            firstname=contact.firstname,
            lastname=contact.lastname,
            patronymic=contact.patronymic,
            phone_number=contact.phone_number,
            telegram_name=contact.telegram_name,
            company_url=f"/api/companies/{contact.company_id}",
        )
