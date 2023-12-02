from sqlmodel import Field, SQLModel

from app.models.validator_regex import email_regex


class CreatorBase(SQLModel):
    created_by: str = Field(regex=email_regex(), nullable=False)
