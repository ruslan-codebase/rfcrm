from pytest import mark
from uuid6 import uuid6


async def login_user(client):
    user_in = {"email": "ivan.ivanov@mail.ru", "password": "Somepass333$"}
    login_data = {"username": "ivan.ivanov@mail.ru", "password": "Somepass333$"}
    _ = await client.post("/api/users/register", json=user_in)
    logged_in = await client.post("/api/users/login", data=login_data)
    token = logged_in.json().get("jwt")
    return {"Authorization": f"Bearer {token}"}


@mark.asyncio
async def test_create_company(async_client):
    async for client in async_client:
        company_in = {"name": "VK", "hh_employer_id": "22222"}
        headers = await login_user(client)
        resp = await client.post("/api/companies/", json=company_in, headers=headers)
        assert resp.status_code == 201
        for k, v in company_in.items():
            assert resp.json().get(k) == v
        assert resp.json().get("id") is not None
        assert resp.json().get("created_at") is not None


@mark.asyncio
async def test_create_company_bad_request(async_client):
    async for client in async_client:
        missing_field = {"name": "Yandex"}
        headers = await login_user(client)
        resp1 = await client.post("/api/companies/", json=missing_field)
        assert resp1.status_code == 401
        resp2 = await client.post(
            "/api/companies/", json=missing_field, headers=headers
        )
        assert resp2.status_code == 422


@mark.asyncio
async def test_get_companies(async_client):
    async for client in async_client:
        headers = await login_user(client)
        resp = await client.get("/api/companies/", headers=headers)
        assert resp is not None
        assert resp.status_code == 200
        assert resp.json() == []


@mark.asyncio
async def test_get_company_by_id(async_client):
    async for client in async_client:
        fakeid = uuid6()
        headers = await login_user(client)

        resp0 = await client.get(f"/api/companies/{fakeid}", headers=headers)
        assert resp0.status_code == 404
        assert resp0.json() == {"detail": "Company not found with given id"}

        company_in = {"name": "Yandex", "hh_employer_id": "12345"}
        added_resp = await client.post(
            "/api/companies/", json=company_in, headers=headers
        )
        company_id = added_resp.json().get("id")

        resp1 = await client.get(f"/api/companies/{company_id}", headers=headers)
        assert resp1.status_code == 200
        for k, v in company_in.items():
            assert resp1.json().get(k) == v

        resp2 = await client.get(f"/api/companies/{company_id}")
        assert resp2.status_code == 401


@mark.asyncio
async def test_delete_company(async_client):
    async for client in async_client:
        company_in = {"name": "Tinkoff", "hh_employer_id": "11111"}
        headers = await login_user(client)

        added_resp = await client.post(
            "/api/companies/", json=company_in, headers=headers
        )
        company_id = added_resp.json().get("id")

        get_resp = await client.get(f"/api/companies/{company_id}", headers=headers)
        assert get_resp.status_code == 200
        assert get_resp.json().get("id") == company_id
        assert get_resp.json().get("name") == "Tinkoff"

        resp1 = await client.delete(f"/api/companies/{company_id}")
        assert resp1.status_code == 401

        resp2 = await client.delete(f"/api/companies/{company_id}", headers=headers)
        assert resp2.status_code == 204

        get_resp2 = await client.get(f"/api/companies/{company_id}", headers=headers)
        assert get_resp2.status_code == 404


@mark.asyncio
async def test_update_company(async_client):
    async for client in async_client:
        company_in = {"name": "Tinkoff", "hh_employer_id": "12234"}
        headers = await login_user(client)

        added_resp = await client.post(
            "/api/companies/", json=company_in, headers=headers
        )
        company_id = added_resp.json().get("id")

        company_update = {"hh_employer_id": "55555"}

        resp0 = await client.put(f"/api/companies/{company_id}", json=company_update)
        assert resp0.status_code == 401

        resp1 = await client.put(
            f"/api/companies/{company_id}", json=company_update, headers=headers
        )
        assert resp1.status_code == 200
        assert resp1.json().get("hh_employer_id") == "55555"

        get_resp = await client.get(f"/api/companies/{company_id}", headers=headers)
        assert get_resp.json().get("hh_employer_id") == "55555"
