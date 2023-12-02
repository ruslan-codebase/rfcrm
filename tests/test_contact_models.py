from datetime import datetime

from pytest import mark, raises
from uuid6 import UUID, uuid6

from app.models.base_model import BaseModel
from app.models.contact import (
    Contact,
    ContactBase,
    ContactIn,
    ContactOut,
    ContactUpdate,
    PhoneBase,
)


@mark.asyncio
async def test_contact_base():
    model = ContactBase(firstname="Ivan", lastname="Ivanov")
    assert model.patronymic is None
    assert model.telegram_name is None
    assert model.company_id is None

    # missing required field
    with raises(ValueError):
        _ = ContactBase(
            firstname="Ivan",
        )


@mark.asyncio
async def test_contact_phone_base():
    too_short = 12354
    not_int = "298434"
    doesnt_start_with_7 = 19998887733
    good_phone = 79998884433

    with raises(ValueError):
        _ = PhoneBase(phone_number=too_short)

    with raises(ValueError):
        _ = PhoneBase(phone_number=not_int)

    with raises(ValueError):
        _ = PhoneBase(phone_number=doesnt_start_with_7)

    model = PhoneBase(phone_number=good_phone)
    assert model.phone_number == good_phone

    model2 = PhoneBase(phone_number=None)
    assert model2.phone_number is None


@mark.asyncio
async def test_contact_in():
    model = ContactIn(firstname="Ivan", lastname="Ivanov", telegram_name="super_ivan")

    assert not hasattr(model, "id")


@mark.asyncio
async def test_contact_update():
    model1 = ContactUpdate()
    for field, value in model1.__dict__.items():
        assert value is None

    # phone too short
    with raises(ValueError):
        _ = ContactUpdate(phone_number=7000)

    # phone doesnt start with 7
    with raises(ValueError):
        _ = ContactUpdate(phone_number=89993332211)

    # phone is not an int
    with raises(ValueError):
        _ = ContactUpdate(phone_number="7hellofjjhh")


@mark.asyncio
async def test_contact():
    model = Contact(
        firtname="John",
        lastname="Doe",
    )

    assert hasattr(model, "id")
    assert hasattr(model, "created_at")
    assert type(model.id) is UUID
    assert type(model.created_at) is datetime
    assert issubclass(Contact, BaseModel)
    assert issubclass(Contact, ContactBase)


@mark.asyncio
async def test_contact_out():
    model = ContactOut(firstname="Ivan", lastname="Ivanov")

    assert hasattr(model, "company_url")
    assert model.firstname == "Ivan"
    assert model.lastname == "Ivanov"
    assert model.patronymic is None
    assert model.phone_number is None
    assert model.telegram_name is None
    assert model.company_url is None

    fakeid = uuid6()
    contact = Contact(firstname="John", lastname="Doe", company_id=fakeid)
    contact_out = ContactOut.from_contact(contact)

    assert contact_out.firstname == "John"
    assert contact_out.lastname == "Doe"
    assert contact_out.company_url == f"/api/companies/{fakeid}"
    assert contact_out.id == contact.id
    assert contact_out.created_at == contact.created_at
