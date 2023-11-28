from typing import Optional
from uuid6 import uuid6, UUID
from sqlmodel import SQLModel, Field
from sqlalchemy.orm import declared_attr
from datetime import datetime


class BaseModel(SQLModel):
    id: UUID = Field(default_factory=uuid6, primary_key=True, nullable=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__
