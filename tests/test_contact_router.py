from pytest import mark
from uuid6 import uuid6


async def login_user(client):
    user_in = {"email": "john.doe@mail.ru", "password": "Helloo33$"}
    login_data = {"username": user_in.get("email"), "password": user_in.get("password")}
    _ = await client.post("/api/users/register", json=user_in)
    logged_in = await client.post("/api/users/login", data=login_data)
    token = logged_in.json().get("jwt")
    return {"Authorization": f"Bearer {token}"}


@mark.asyncio
async def test_create_contact(async_client):
    async for client in async_client:
        contact_in = {"firstname": "John", "lastname": "Ivanov"}
        headers = await login_user(client)
        resp = await client.post("/api/contacts/", json=contact_in, headers=headers)
        assert resp.status_code == 201
        for k, v in contact_in.items():
            assert resp.json().get(k) == v

        with_optional_values = {
            "firstname": "Ivan",
            "lastname": "Doe",
            "patronymic": "Ivanovich",
            "telegram_name": "ivan_doe_epic",
        }
        resp2 = await client.post(
            "/api/contacts/", json=with_optional_values, headers=headers
        )
        assert resp2.status_code == 201
        for k, v in with_optional_values.items():
            assert resp2.json().get(k) == v

        company_in = {"name": "Yandex", "hh_employer_id": "22223"}
        company_resp = await client.post(
            "/api/companies/", json=company_in, headers=headers
        )
        with_company = {
            "firstname": "Ivan",
            "lastname": "Ivanov",
            "company_id": company_resp.json().get("id"),
        }
        resp3 = await client.post("/api/contacts/", json=with_company, headers=headers)
        assert resp3.status_code == 201
        assert resp3.json().get("firstname") == "Ivan"
        assert resp3.json().get("lastname") == "Ivanov"
        assert (
            resp3.json().get("company_url")
            == f"/api/companies/{company_resp.json().get('id')}"
        )


@mark.asyncio
async def test_create_contact_bad_request(async_client):
    async for client in async_client:
        missing_field = {"firsname": "Boris"}
        headers = await login_user(client)
        resp0 = await client.post("/api/contacts/", json=missing_field, headers=headers)
        assert resp0.status_code == 422

        bad_id = {
            "firstname": "Ivan",
            "lastname": "Ivanov",
            "company_id": "very-bad-id",
        }
        resp1 = await client.post("/api/contacts/", json=bad_id, headers=headers)
        assert resp1.status_code == 422

        non_existing_id = {
            "firstname": "Ivan",
            "lastname": "Ivanov",
            "company_id": str(uuid6()),
        }
        resp2 = await client.post(
            "/api/contacts/", json=non_existing_id, headers=headers
        )
        assert resp2.status_code == 404

        bad_phone_number = {
            "firstname": "Ivan",
            "lastname": "Ivanov",
            "phone_number": "22345",
        }
        resp3 = await client.post(
            "/api/contacts/", json=bad_phone_number, headers=headers
        )
        assert resp3.status_code == 422


@mark.asyncio
async def test_get_contacts(async_client):
    async for client in async_client:
        headers = await login_user(client)
        resp = await client.get("/api/contacts/", headers=headers)
        assert resp.status_code == 200
        assert resp.json() == []

        add_resp = await client.post(
            "/api/contacts/",
            json={"firstname": "Ivan", "lastname": "Ivanov"},
            headers=headers,
        )
        assert add_resp.status_code == 201
        resp2 = await client.get("/api/contacts/", headers=headers)
        assert resp2.status_code == 200
        assert resp2.json()[0].get("firstname") == "Ivan"
        assert resp2.json()[0].get("lastname") == "Ivanov"
        assert resp2.json()[0].get("id") is not None


@mark.asyncio
async def test_get_contact_by_id(async_client):
    async for client in async_client:
        fakeid = uuid6()
        headers = await login_user(client)
        resp0 = await client.get(f"/api/contacts/{fakeid}", headers=headers)
        assert resp0.status_code == 404

        add_resp = await client.post(
            "/api/contacts/",
            json={"firstname": "John", "lastname": "Doe", "telegram_name": "some_name"},
            headers=headers,
        )
        contact_id = add_resp.json().get("id")

        resp1 = await client.get(f"/api/contacts/{contact_id}", headers=headers)
        assert resp1.status_code == 200
        assert resp1.json().get("id") == add_resp.json().get("id")
        assert resp1.json().get("firstname") == "John"
        assert resp1.json().get("lastname") == "Doe"


@mark.asyncio
async def test_delete_contact(async_client):
    async for client in async_client:
        headers = await login_user(client)
        notfound = await client.delete(f"/api/contacts/{str(uuid6())}", headers=headers)
        assert notfound.status_code == 404

        add_resp = await client.post(
            "/api/contacts/",
            json={"firstname": "Jack", "lastname": "Reacher"},
            headers=headers,
        )
        contact_id = add_resp.json().get("id")

        get1 = await client.get(f"/api/contacts/{contact_id}", headers=headers)
        assert get1.status_code == 200
        assert get1.json().get("id") == contact_id
        assert get1.json().get("firstname") == "Jack"

        resp = await client.delete(f"/api/contacts/{contact_id}", headers=headers)
        assert resp.status_code == 204

        get2 = await client.get(f"/api/contacts/{contact_id}", headers=headers)
        assert get2.status_code == 404
