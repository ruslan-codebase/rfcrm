from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from app.models.validator_regex import email_regex, password_regex


class UserBase(SQLModel):
    email: str = Field(regex=email_regex(), primary_key=True, nullable=False)


class UserIn(UserBase):
    password: str = Field(regex=password_regex())


class User(UserBase, table=True):
    password_hash: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
