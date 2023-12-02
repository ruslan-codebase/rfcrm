from fastapi import HTTPException
from pytest import mark, raises
from sqlalchemy import select
from uuid6 import uuid6

from app.models.company import Company, CompanyIn, CompanyUpdate
from app.services.company_service import CompanyService


def simple_company(suffix="") -> CompanyIn:
    return CompanyIn(name=f"Tinkoff{suffix}", hh_employer_id=f"11111{suffix}")


@mark.asyncio
async def test_create_company(async_session):
    async for s in async_session:
        service = CompanyService(s)
        fake_email = "ivan.ivanov@mail.ru"

        before = await s.execute(select(Company))
        assert len(before.scalars().all()) == 0

        result = await service.create(simple_company(), fake_email)
        assert type(result) is Company
        assert result.id is not None
        assert result.created_at is not None
        assert result.created_by == fake_email
        assert result.name == "Tinkoff"
        assert result.hh_employer_id == "11111"

        after = await s.execute(select(Company))
        after = after.scalars().all()
        assert len(after) == 1
        assert after[0].id == result.id


@mark.asyncio
async def test_get_company_by_id(async_session):
    async for s in async_session:
        service = CompanyService(s)
        fake_email = "ivan.ivanov@mail.ru"
        email2 = "some.one@else.com"
        company = await service.create(simple_company(), fake_email)

        with raises(HTTPException):
            _ = await service.get_by_id(company.id, email2)

        result = await service.get_by_id(company.id, fake_email)

        assert type(result) is Company
        assert result.id == company.id
        assert result.created_at == company.created_at
        assert result.created_by == company.created_by
        assert result.name == company.name
        assert result.hh_employer_id == company.hh_employer_id
        assert result == company


@mark.asyncio
async def test_company_not_found(async_session):
    async for s in async_session:
        service = CompanyService(s)
        fakeid = uuid6()
        fake_email = "ivan.ivanov@mail.ru"

        with raises(HTTPException):
            _ = await service.get_by_id(fakeid, fake_email)

        with raises(HTTPException):
            _ = await service.delete(fakeid, fake_email)

        with raises(HTTPException):
            _ = await service.update(fakeid, fake_email, CompanyUpdate(name="newname"))


@mark.asyncio
async def test_get_companies(async_session):
    async for s in async_session:
        service = CompanyService(s)
        fake_email = "ivan.ivanov@mail.ru"
        email2 = "ifqsd.flksj@fsqdfq.com"

        result1 = await service.get(fake_email)
        assert type(result1) is list
        assert len(result1) == 0

        for i in range(22):
            _ = await service.create(simple_company(suffix=i), fake_email)

        result2 = await service.get(fake_email)
        assert len(result2) == 20

        result3 = await service.get(fake_email, limit=30)
        assert len(result3) == 22

        result3 = await service.get(fake_email, offset=1, limit=25)
        assert len(result3) == 21

        result4 = await service.get(email2)
        assert len(result4) == 0


@mark.asyncio
async def test_delete_company(async_session):
    async for s in async_session:
        service = CompanyService(s)
        fake_email = "ivan.ivanov@mail.ru"
        email2 = "mlsdqf.flskjqd@qfsjdf.com"
        company = await service.create(simple_company(), fake_email)

        result1 = await s.get(Company, company.id)
        assert result1 == company

        with raises(HTTPException):
            _ = await service.delete(company.id, email2)

        delete_result = await service.delete(company.id, fake_email)
        assert delete_result == company.id

        result2 = await s.get(Company, company.id)
        assert result2 is None


@mark.asyncio
async def test_update_company(async_session):
    async for s in async_session:
        service = CompanyService(s)
        fake_email = "ivan.ivanov@mail.ru"
        email2 = "qsdf.fqsd@fkqdf.com"
        company = await service.create(simple_company(), fake_email)

        assert company.name == "Tinkoff"
        assert company.hh_employer_id == "11111"

        with raises(HTTPException):
            _ = await service.update(company.id, email2, CompanyUpdate())

        result0 = await service.update(company.id, fake_email, CompanyUpdate())
        assert result0 == company
        assert result0.name == "Tinkoff"
        assert result0.hh_employer_id == "11111"

        result1 = await service.update(
            company.id, fake_email, CompanyUpdate(name="hellooo")
        )
        assert result1 == company
        assert company.name == "hellooo"
        assert company.hh_employer_id == "11111"

        _ = await service.update(
            company.id, fake_email, CompanyUpdate(hh_employer_id="12345")
        )
        assert company.name == "hellooo"
        assert company.hh_employer_id == "12345"

        _ = await service.update(
            company.id, fake_email, CompanyUpdate(name="ducky", hh_employer_id="11111")
        )
        assert company.name == "ducky"
        assert company.hh_employer_id == "11111"
