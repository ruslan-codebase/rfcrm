from datetime import datetime
from typing import Optional

from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel
from uuid6 import UUID, uuid6


class BaseModel(SQLModel):
    id: UUID = Field(default_factory=uuid6, primary_key=True, nullable=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__
