from datetime import datetime

from pydantic import ValidationError
from pytest import mark, raises

from app.models.user import User, UserIn


@mark.asyncio
async def test_user_password_validator():
    not_long_enough = "aAbb3$"
    no_uppercase = "aze233$errez"
    no_lowercase = "FDHJKF345$22"
    no_special_char = "sdfsdf24353FDMLFJ"
    good_password = "azbJIF23&"
    email = "some.dude@mail.com"

    with raises(ValidationError):
        _ = UserIn(email=email, password=not_long_enough)

    with raises(ValidationError):
        _ = UserIn(email=email, password=no_uppercase)

    with raises(ValidationError):
        _ = UserIn(email=email, password=no_lowercase)

    with raises(ValidationError):
        _ = UserIn(email=email, password=no_special_char)

    user_in = UserIn(email=email, password=good_password)

    assert user_in.email == email
    assert user_in.password == good_password


@mark.asyncio
async def test_email_validator():
    bad_char_in_local = "hello$world@mail.ru"
    no_at_sign = "hello.world.something.com"
    top_level_too_long = "john.doe@mail.jacksson"
    has_trailing_dot = "helloo.@outlook.com"
    has_doudle_dot = "hello..me@mail.ru"
    has_leading_dot = ".me.me.me@mail.ru"
    good_email = "name_name2@company.mail.com"
    password = "afh334JHD$F"

    with raises(ValueError):
        _ = UserIn(email=bad_char_in_local, password=password)

    with raises(ValueError):
        _ = UserIn(email=no_at_sign, password=password)

    with raises(ValueError):
        _ = UserIn(email=top_level_too_long, password=password)

    with raises(ValueError):
        _ = UserIn(email=has_trailing_dot, password=password)

    with raises(ValueError):
        _ = UserIn(email=has_doudle_dot, password=password)

    with raises(ValueError):
        _ = UserIn(email=has_leading_dot, password=password)

    user_in = UserIn(email=good_email, password=password)

    assert user_in.email == good_email


@mark.asyncio
async def test_user_model():
    user = User(
        email="some.dude@mail.com",
        password_hash="fmsqdlfjmqlk43093HK3N34H",
    )
    assert user.created_at is not None
    assert type(user.created_at) is datetime
