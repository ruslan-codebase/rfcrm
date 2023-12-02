from datetime import datetime

from pytest import mark, raises
from uuid6 import UUID

from app.models.base_model import BaseModel
from app.models.company import Company, CompanyBase, CompanyIn, CompanyOut, CreatorBase


@mark.asyncio
async def test_company_base():
    model = CompanyBase(name="Контур", hh_employer_id="41862")

    assert model.http_link == "https://hh.ru/employer/41862"
    assert model.name == "Контур"
    assert model.hh_employer_id == "41862"


@mark.asyncio
async def test_company_creator_base():
    fake_email = "ivan.ivanov@mail.ru"
    model = CreatorBase(created_by=fake_email)

    with raises(ValueError):
        _ = CreatorBase(created_by=None)

    assert model.created_by == fake_email


@mark.asyncio
async def test_company_in():
    model = CompanyIn(name="Контур", hh_employer_id="41862")

    assert hasattr(model, "id") is False
    assert hasattr(model, "created_at") is False


@mark.asyncio
async def test_company():
    fake_email = "ivan.ivanov@mail.ru"
    model = Company(name="Контур", hh_employer_id="41862", created_by=fake_email)

    assert hasattr(model, "id")
    assert hasattr(model, "created_at")
    assert model.created_by == fake_email
    assert type(model.id) is UUID
    assert type(model.created_at) is datetime
    assert issubclass(Company, BaseModel)
    assert issubclass(Company, CompanyBase)


@mark.asyncio
async def test_company_out():
    model = CompanyOut(name="Yandex", hh_employer_id="122345")

    assert model.name == "Yandex"
    assert model.hh_employer_id == "122345"
    assert model.created_at is not None
    assert model.id is not None

    company = Company(name="VK", hh_employer_id="33992")
    company_out = CompanyOut.from_company(company)

    assert company_out.name == company.name
    assert company_out.hh_employer_id == company.hh_employer_id
    assert company_out.created_at == company.created_at
    assert company_out.id == company.id
    assert not hasattr(company_out, "created_by")
