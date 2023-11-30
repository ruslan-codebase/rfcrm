import time
from datetime import timedelta

from fastapi import HTTPException
from pytest import mark, raises

from app.models.user import User, UserIn
from app.services.user_service import UserService


@mark.asyncio
async def test_register_user(async_session):
    async for s in async_session:
        service = UserService(s)
        user_in = UserIn(email="john.doe@mail.ru", password="MyBestPass1$")

        before = await s.get(User, user_in.email)
        assert before is None

        user = await service.register(user_in)
        assert user.email == user_in.email
        assert user.password_hash != user_in.password

        after = await s.get(User, user_in.email)
        assert after == user


@mark.asyncio
async def test_login_user(async_session):
    async for s in async_session:
        service = UserService(s)
        user_in = UserIn(email="john.doe@mail.ru", password="MyBestPass1$")
        wrong_pass = UserIn(email="john.doe@mail.ru", password="Something2&")

        # user doesnt exist
        with raises(HTTPException):
            _ = await service.login(user_in)

        _ = await service.register(user_in)

        with raises(HTTPException):
            _ = await service.login(wrong_pass)

        token = await service.login(user_in)
        assert token is not None
        assert type(token) is str


@mark.asyncio
async def test_get_logged_in_user(async_session):
    async for s in async_session:
        service = UserService(s)
        user_in = UserIn(email="john.doe@mail.ru", password="SomePass35$")
        user = await service.register(user_in)
        token = await service.login(user_in, timedelta(microseconds=1))

        time.sleep(2)

        # expired
        with raises(HTTPException):
            _ = await service.get_logged_in_user(token)

        token = await service.login(user_in)

        # wrong token
        with raises(HTTPException):
            _ = await service.get_logged_in_user(token + "fsd")

        logged_in = await service.get_logged_in_user(token)
        assert logged_in.email == user.email
        assert logged_in.password_hash == user.password_hash
        assert logged_in.created_at == user.created_at
