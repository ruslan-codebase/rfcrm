from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import PositiveInt, validator
from uuid6 import UUID
from app.models.base_model import BaseModel


class ContactBase(SQLModel):
    firstname: str
    lastname: str
    patronymic: Optional[str]
    telegram_name: Optional[str]
    phone_number: Optional[str]
    company_id: Optional[UUID] = Field(default=None, foreign_key="Company.id")

    @validator("phone_number")
    def phone_validation(cls, v):
        str_v = str(v)

        if not str_v.startswith("7"):
            raise ValueError("Phone number must start with 7")
        
        if len(str_v) != 11:
            # 1 digit country code
            # 3 digits region code
            # 7 digits phone number
            raise ValueError("Phone number must be 11 digits long.")

        return v


class Contact(BaseModel, ContactBase, table=True):
    pass


class ContactIn(ContactBase):
    pass


class ContactUpdate(SQLModel):
    firstname: Optional[str]
    lastname: Optional[str]
    patronymic: Optional[str]
    telegram_name: Optional[str]
    phone_number: Optional[str]
    company_id: Optional[UUID]

    @validator("phone_number")
    def phone_validation(cls, v):
        str_v = str(v)

        if not str_v.starts_with("7"):
            raise ValueError("Phone number must start with 7")
        
        if len(str_v) != 11:
            # 1 digit country code
            # 3 digits region code
            # 7 digits phone number
            raise ValueError("Phone number must be 11 digits long.")

        return v