from pytest import mark, raises
from uuid6 import UUID
from datetime import datetime
from app.models.contact import ContactBase, Contact, ContactIn, ContactUpdate
from app.models.base_model import BaseModel


@mark.asyncio
async def test_contact_base():
    model = ContactBase(
        firstname = "Ivan",
        lastname = "Ivanov"
    )
    assert model.patronymic is None
    assert model.telegram_name is None
    assert model.phone_number is None
    assert model.company_id is None

    # phone too short
    with raises(ValueError):
        bad_phone_model = ContactBase(
            firstname = "Ivan",
            lastname = "Ivanov",
            phone_number = 79999
        )
    
    # phone doesnt start with country code 7
    with raises(ValueError):
        bad_phone_model2 = ContactBase(
            firstname = "Ivan",
            lastname = "Ivanov",
            phone_number = 19998882233
        )

    # phone oke
    good_phone_number = ContactBase(
        firstname = "Ivan",
        lastname = "Ivanov",
        phone_number = 79997774422
    )

    # missing required field
    with raises(ValueError):
        _ = ContactBase(firstname = "Ivan",)


@mark.asyncio
async def test_contact_in():
    model = ContactIn(
        firstname="Ivan",
        lastname="Ivanov",
        telegram_name="super_ivan"
    )

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
        firtname = "John",
        lastname = "Doe",
    )

    assert hasattr(model, "id")
    assert hasattr(model, "created_at")
    assert type(model.id) is UUID
    assert type(model.created_at) is datetime
    assert issubclass(Contact, BaseModel)
    assert issubclass(Contact, ContactBase)

