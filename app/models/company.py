from typing import Optional

from sqlmodel import SQLModel

from app.models.base_model import BaseModel


class CreatorBase(SQLModel):
    created_by: str


class CompanyBase(SQLModel):
    name: str
    hh_employer_id: str

    @property
    def http_link(self) -> str:
        return f"https://hh.ru/employer/{self.hh_employer_id}"


class Company(BaseModel, CompanyBase, CreatorBase, table=True):
    pass


class CompanyIn(CompanyBase):
    pass


class CompanyUpdate(SQLModel):
    name: Optional[str]
    hh_employer_id: Optional[str]


class CompanyOut(BaseModel, CompanyBase):
    pass

    @staticmethod
    def from_company(company: Company):
        return CompanyOut(
            id=company.id,
            created_at=company.created_at,
            name=company.name,
            hh_employer_id=company.hh_employer_id,
        )
