from pytest import mark
from tests.fixtures import async_session
from app.models.company import Company, CompanyIn, CompanyUpdate
from app.services.company_service import CompanyService


@mark.asyncio
async def test_create_company(async_session):
    async for s in async_session:
        service = CompanyService(s)
        company_in = CompanyIn(
            name = "Awesome Company",
            hh_employer_id = "12345"
        )
        result = await service.create(company_in)

        assert type(result) is Company
        assert result.id is not None
        assert result.created_at is not None
        assert result.name == company_in.name
        assert result.hh_employer_id == company_in.hh_employer_id

@mark.asyncio
async def test_get_company_by_id(async_session):
    async for s in async_session:
        service = CompanyService(s)
        company_in = CompanyIn(
            name = "Awesome Company",
            hh_employer_id = "12345"
        )
        company = await service.create(company_in)
        result = await service.get_by_id(company.id)

        assert type(result) is Company
        assert result.id == company.id
        assert result.created_at == company.created_at
        assert result.name == company.name
        assert result.hh_employer_id == company.hh_employer_id
        assert result == company

@mark.asyncio
async def test_get_companies(async_session):
    async for s in async_session:
        service = CompanyService(s)
        result1 = await service.get()

        assert type(result1) is list
        assert len(result1) == 0

        company = await service.create(
            CompanyIn(
                name = "Awesome Company",
                hh_employer_id = "12345"
            )
        )
        result2 = await service.get()

        assert len(result2) == 1
        assert result2[0] == company

        for i in range(22):
            c = await service.create(
                CompanyIn(
                    name = f"A{i}",
                    hh_employer_id = f"1234{i}"
                )
            )
        
        result3 = await service.get()
        # test default item limit
        assert len(result3) == 20

        result4 = await service.get(limit=30)
        assert len(result4) == 23

        result5 = await service.get(offset=1, limit=25)
        assert len(result5) == 22

@mark.asyncio
async def test_delete_company(async_session):
    async for s in async_session:
        service = CompanyService(s)
        company = await service.create(
            CompanyIn(
                name = "companyname",
                hh_employer_id = "132345"
            )
        )

        result1 = await service.get_by_id(company.id)
        assert result1 == company

        await service.delete(company.id)

        result2 = await service.get_by_id(company.id)
        assert result2 is None

@mark.asyncio
async def test_update_company(async_session):
    async for s in async_session:
        service = CompanyService(s)
        company = await service.create(
            CompanyIn(
                name = "companyname",
                hh_employer_id = "23478"
            )
        )
        result0 = await service.update(
            company.id,
            CompanyUpdate()
        )
        assert result0 == company

        result1 = await service.update(
            company.id,
            CompanyUpdate(
                name = "hellooo"
            )
        )
        assert result1 == company
        assert company.name == "hellooo"
        assert company.hh_employer_id == "23478"

        result2 = await service.update(
            company.id,
            CompanyUpdate(
                hh_employer_id = "12345"
            )
        )
        assert company.name == "hellooo"
        assert company.hh_employer_id == "12345"

        result3 = await service.update(
            company.id,
            CompanyUpdate(
                name = "ducky",
                hh_employer_id = "11111"
            )
        )
        assert company.name == "ducky"
        assert company.hh_employer_id == "11111"
