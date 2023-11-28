from pytest import mark
from uuid6 import uuid6


@mark.asyncio
async def test_create_contact(async_client):
    async for client in async_client:
        contact_in = {"firstname": "John", "lastname": "Ivanov"}
        resp = await client.post("/api/contacts/", json=contact_in)
        assert resp.status_code == 201
        for k, v in contact_in.items():
            assert resp.json().get(k) == v

        with_optional_values = {
            "firstname": "Ivan",
            "lastname": "Doe",
            "patronymic": "Ivanovich",
            "telegram_name": "ivan_doe_epic",
        }
        resp2 = await client.post("/api/contacts/", json=with_optional_values)
        assert resp2.status_code == 201
        for k, v in with_optional_values.items():
            assert resp2.json().get(k) == v

        company_in = {"name": "Yandex", "hh_employer_id": "22223"}
        company_resp = await client.post("/api/companies/", json=company_in)
        company_data = company_resp.json().get("data")
        with_company = {
            "firstname": "Ivan",
            "lastname": "Ivanov",
            "company_id": company_data.get("id"),
        }
        resp3 = await client.post("/api/contacts/", json=with_company)
        assert resp3.status_code == 201
        for k, v in with_company.items():
            assert resp3.json().get(k) == v


@mark.asyncio
async def test_create_contact_bad_request(async_client):
    async for client in async_client:
        missing_field = {"firsname": "Boris"}
        resp0 = await client.post("/api/contacts/", json=missing_field)
        assert resp0.status_code == 422

        bad_id = {
            "firstname": "Ivan",
            "lastname": "Ivanov",
            "company_id": "very-bad-id",
        }
        resp1 = await client.post("/api/contacts/", json=bad_id)
        assert resp1.status_code == 422

        non_existing_id = {
            "firstname": "Ivan",
            "lastname": "Ivanov",
            "company_id": str(uuid6()),
        }
        resp2 = await client.post("/api/contacts/", json=non_existing_id)
        assert resp2.status_code == 404

        bad_phone_number = {
            "firstname": "Ivan",
            "lastname": "Ivanov",
            "phone_number": "22345",
        }
        resp3 = await client.post("/api/contacts/", json=bad_phone_number)
        assert resp3.status_code == 422


@mark.asyncio
async def test_get_contacts(async_client):
    async for client in async_client:
        resp = await client.get("/api/contacts/")
        assert resp.status_code == 200
        assert resp.json() == []

        add_resp = await client.post(
            "/api/contacts/", json={"firstname": "Ivan", "lastname": "Ivanov"}
        )
        assert add_resp.status_code == 201
        resp2 = await client.get("/api/contacts/")
        assert resp2.status_code == 200
        assert resp2.json()[0].get("firstname") == "Ivan"
        assert resp2.json()[0].get("lastname") == "Ivanov"
        assert resp2.json()[0].get("id") is not None


@mark.asyncio
async def test_get_contact_by_id(async_client):
    async for client in async_client:
        fakeid = uuid6()
        resp0 = await client.get(f"/api/contacts/{fakeid}")
        assert resp0.status_code == 404

        add_resp = await client.post(
            "/api/contacts/",
            json={"firstname": "John", "lastname": "Doe", "telegram_name": "some_name"},
        )
        contact_id = add_resp.json().get("id")

        resp1 = await client.get(f"/api/contacts/{contact_id}")
        assert resp1.status_code == 200
        assert resp1.json().get("id") == add_resp.json().get("id")
        assert resp1.json().get("firstname") == "John"
        assert resp1.json().get("lastname") == "Doe"


@mark.asyncio
async def test_delete_contact(async_client):
    async for client in async_client:
        notfound = await client.delete(f"/api/contacts/{str(uuid6())}")
        assert notfound.status_code == 404

        add_resp = await client.post(
            "/api/contacts/", json={"firstname": "Jack", "lastname": "Reacher"}
        )
        contact_id = add_resp.json().get("id")

        get1 = await client.get(f"/api/contacts/{contact_id}")
        assert get1.status_code == 200
        assert get1.json().get("id") == contact_id
        assert get1.json().get("firstname") == "Jack"

        resp = await client.delete(f"/api/contacts/{contact_id}")
        assert resp.status_code == 200
        assert resp.json().get("message") == "successfully deleted"

        get2 = await client.get(f"/api/contacts/{contact_id}")
        assert get2.status_code == 404
