from pytest import mark
from uuid6 import uuid6


@mark.asyncio
async def test_create_company(async_client):
    async for client in async_client:
        company_in = {"name": "VK", "hh_employer_id": "22222"}
        resp = await client.post("/api/companies/", json=company_in)
        assert resp.status_code == 201
        data = resp.json().get("data")
        for k, v in company_in.items():
            assert data.get(k) == v
        assert data.get("id") is not None
        assert data.get("created_at") is not None


@mark.asyncio
async def test_create_company_bad_request(async_client):
    async for client in async_client:
        missing_field = {"name": "Yandex"}
        resp1 = await client.post("/api/companies/", json=missing_field)
        assert resp1.status_code == 422

        extra_field = {
            "name": "Yandex",
            "hh_employer_id": "22234",
            "something": "very interesting",
        }
        resp2 = await client.post("/api/companies/", json=extra_field)
        assert resp2.status_code == 201


@mark.asyncio
async def test_get_companies(async_client):
    async for client in async_client:
        resp = await client.get("/api/companies/")
        assert resp is not None
        assert resp.status_code == 200
        assert resp.json() == {"data": [], "message": ""}


@mark.asyncio
async def test_get_company_by_id(async_client):
    async for client in async_client:
        fakeid = uuid6()
        resp0 = await client.get(f"/api/companies/{fakeid}")
        assert resp0.status_code == 404
        assert resp0.json() == {"detail": "Company not found with given id"}

        company_in = {"name": "Yandex", "hh_employer_id": "12345"}
        added_resp = await client.post("/api/companies/", json=company_in)
        company_id = added_resp.json().get("data").get("id")
        resp1 = await client.get(f"/api/companies/{company_id}")
        assert resp1.status_code == 200
        data = resp1.json().get("data")
        for k, v in company_in.items():
            assert data.get(k) == v


@mark.asyncio
async def test_delete_company(async_client):
    async for client in async_client:
        company_in = {"name": "Tinkoff", "hh_employer_id": "11111"}
        added_resp = await client.post("/api/companies/", json=company_in)
        company_id = added_resp.json().get("data").get("id")
        get_resp = await client.get(f"/api/companies/{company_id}")
        assert get_resp.status_code == 200
        data = get_resp.json().get("data")
        assert data.get("id") == company_id
        assert data.get("name") == "Tinkoff"
        resp1 = await client.delete(f"/api/companies/{company_id}")
        assert resp1.status_code == 204
        get_resp2 = await client.get(f"/api/companies/{company_id}")
        assert get_resp2.status_code == 404


@mark.asyncio
async def test_update_company(async_client):
    async for client in async_client:
        company_in = {"name": "Tinkoff", "hh_employer_id": "12234"}
        added_resp = await client.post("/api/companies/", json=company_in)
        company_id = added_resp.json().get("data").get("id")

        company_update = {"hh_employer_id": "55555"}
        resp0 = await client.put(f"/api/companies/{company_id}", json=company_update)
        assert resp0.status_code == 200
        assert resp0.json().get("data").get("hh_employer_id") == "55555"

        get_resp = await client.get(f"/api/companies/{company_id}")
        assert get_resp.json().get("data").get("hh_employer_id") == "55555"
