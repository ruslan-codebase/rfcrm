from pytest import mark
from uuid6 import UUID
from datetime import datetime
from app.models.company import CompanyBase, Company, CompanyIn
from app.models.base_model import BaseModel


@mark.asyncio
async def test_company_base():
    model = CompanyBase(name="Контур", hh_employer_id="41862")

    assert model.http_link == "https://hh.ru/employer/41862"


@mark.asyncio
async def test_company_in():
    model = CompanyIn(name="Контур", hh_employer_id="41862")

    assert hasattr(model, "id") is False
    assert hasattr(model, "created_at") is False


@mark.asyncio
async def test_company():
    model = Company(name="Контур", hh_employer_id="41862")

    assert hasattr(model, "id")
    assert hasattr(model, "created_at")
    assert type(model.id) is UUID
    assert type(model.created_at) is datetime
    assert issubclass(Company, BaseModel)
    assert issubclass(Company, CompanyBase)
