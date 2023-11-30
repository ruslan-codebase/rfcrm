from pytest import mark


@mark.asyncio
async def test_register_user(async_client):
    async for client in async_client:
        user_in = {"email": "john.doe@mail.ru", "password": "GeeGee23$"}
        bad_email = {"email": "john.doe@mail.fmlkqsdf", "password": "GeeGee23$"}
        bad_password = {"email": "john.doe@mail.ru", "password": "fjdksfjqm"}

        resp0 = await client.post("/api/users/register", json=bad_email)
        assert resp0.status_code == 422

        resp1 = await client.post("/api/users/register", json=bad_password)
        assert resp1.status_code == 422

        resp2 = await client.post("/api/users/register", json=user_in)
        assert resp2.status_code == 201
        assert resp2.json().get("email") == user_in.get("email")
        assert resp2.json().get("password_hash") != user_in.get("password")


@mark.asyncio
async def test_login_user(async_client):
    async for client in async_client:
        login_data = {"username": "john.doe@mail.ru", "password": "GeeGee233$"}
        user_in = {"email": "john.doe@mail.ru", "password": "GeeGee233$"}

        resp0 = await client.post("/api/users/login", data=login_data)
        assert resp0.status_code == 404

        _ = await client.post("/api/users/register", json=user_in)
        resp1 = await client.post("/api/users/login", data=login_data)
        assert resp1.status_code == 200
        assert resp1.json().get("jwt") is not None
