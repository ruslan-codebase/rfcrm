from pytest import mark


async def login_user(client):
    user_in = {"email": "ivan.ivanov@mail.ru", "password": "Somepass333$"}
    login_data = {"username": "ivan.ivanov@mail.ru", "password": "Somepass333$"}
    _ = await client.post("/api/users/register", json=user_in)
    logged_in = await client.post("/api/users/login", data=login_data)
    token = logged_in.json().get("jwt")
    return {"Authorization": f"Bearer {token}"}


@mark.asyncio
async def test_create_companies_from_vacancy_search(async_client):
    async for client in async_client:
        headers = await login_user(client)

        resp = await client.get("/api/hh/update-companies", headers=headers)
        assert resp.status_code == 202

        get_resp = await client.get("/api/companies/", headers=headers)
        assert get_resp.status_code == 200
        assert len(get_resp.json()) > 0
