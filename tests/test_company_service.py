from pytest import mark
from tests.fixtures import async_session
from uuid6 import uuid6
from app.models.company import Company, CompanyIn, CompanyUpdate
from app.services.company_service import CompanyService


def simple_company(suffix="") -> CompanyIn:
    return CompanyIn(name=f"Tinkoff{suffix}", hh_employer_id=f"11111{suffix}")


@mark.asyncio
async def test_create_company(async_session):
    async for s in async_session:
        service = CompanyService(s)
        result = await service.create(simple_company())

        assert type(result) is Company
        assert result.id is not None
        assert result.created_at is not None
        assert result.name == "Tinkoff"
        assert result.hh_employer_id == "11111"


@mark.asyncio
async def test_get_company_by_id(async_session):
    async for s in async_session:
        service = CompanyService(s)
        company = await service.create(simple_company())
        result = await service.get_by_id(company.id)

        assert type(result) is Company
        assert result.id == company.id
        assert result.created_at == company.created_at
        assert result.name == company.name
        assert result.hh_employer_id == company.hh_employer_id
        assert result == company


@mark.asyncio
async def test_company_not_found(async_session):
    async for s in async_session:
        service = CompanyService(s)
        fakeid = uuid6()

        get_result = await service.get_by_id(fakeid)
        assert get_result is None

        delete_result = await service.delete(fakeid)
        assert delete_result is None

        company_update = CompanyUpdate(name="newname")
        update_result = await service.update(fakeid, company_update)
        assert update_result is None


@mark.asyncio
async def test_get_companies(async_session):
    async for s in async_session:
        service = CompanyService(s)

        result1 = await service.get()
        assert type(result1) is list
        assert len(result1) == 0

        for i in range(22):
            _ = await service.create(simple_company(suffix=i))

        result2 = await service.get()
        assert len(result2) == 20

        result3 = await service.get(limit=30)
        assert len(result3) == 22

        result3 = await service.get(offset=1, limit=25)
        assert len(result3) == 21


@mark.asyncio
async def test_delete_company(async_session):
    async for s in async_session:
        service = CompanyService(s)
        company = await service.create(simple_company())

        result1 = await service.get_by_id(company.id)
        assert result1 == company

        delete_result = await service.delete(company.id)
        assert delete_result == company.id

        result2 = await service.get_by_id(company.id)
        assert result2 is None


@mark.asyncio
async def test_update_company(async_session):
    async for s in async_session:
        service = CompanyService(s)
        company = await service.create(simple_company())

        result0 = await service.update(company.id, CompanyUpdate())
        assert result0 == company

        result1 = await service.update(company.id, CompanyUpdate(name="hellooo"))
        assert result1 == company
        assert company.name == "hellooo"
        assert company.hh_employer_id == "11111"

        result2 = await service.update(
            company.id, CompanyUpdate(hh_employer_id="12345")
        )
        assert company.name == "hellooo"
        assert company.hh_employer_id == "12345"

        result3 = await service.update(
            company.id, CompanyUpdate(name="ducky", hh_employer_id="11111")
        )
        assert company.name == "ducky"
        assert company.hh_employer_id == "11111"
