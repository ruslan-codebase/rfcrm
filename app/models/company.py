from typing import Optional
from sqlmodel import SQLModel
from app.models.base_model import BaseModel


class CompanyBase(SQLModel):
    name: str
    hh_employer_id: str

    @property
    def http_link(self) -> str:
        return f"https://hh.ru/employer/{self.hh_employer_id}"


class Company(BaseModel, CompanyBase, table=True):
    pass


class CompanyIn(CompanyBase):
    pass


class CompanyUpdate(SQLModel):
    name: Optional[str]
    hh_employer_id: Optional[str]
