from fastapi import HTTPException
from pytest import mark, raises
from uuid6 import uuid6

from app.models.contact import Contact, ContactIn, ContactUpdate
from app.services.contact_service import ContactService


def simple_contact(suffix="") -> ContactIn:
    return ContactIn(firstname=f"Ivan{suffix}", lastname=f"Ivanov{suffix}")


def contact_with_phone_number() -> ContactIn:
    return ContactIn(firstname="Ivan", lastname="Ivanov", phone_number=79998887766)


def company_contact(c_id) -> ContactIn:
    return ContactIn(firstname="Ivan", lastname="Ivanov", company_id=c_id)


@mark.asyncio
async def test_create_contact(async_session):
    async for s in async_session:
        service = ContactService(s)
        fake_email = "john.doe@gmail.com"

        before = await service.get(fake_email)
        assert len(before) == 0

        result = await service.create(simple_contact(), fake_email)
        assert type(result) is Contact
        assert result.id is not None
        assert result.created_at is not None

        after = await service.get(fake_email)
        assert len(after) == 1
        assert after[0].id == result.id


@mark.asyncio
async def test_get_contacts(async_session):
    async for s in async_session:
        service = ContactService(s)
        fake_email = "john.doe@gmail.com"

        empty = await service.get(fake_email)
        assert type(empty) is list
        assert len(empty) == 0

        for i in range(22):
            _ = await service.create(simple_contact(suffix=str(i)), fake_email)

        default_limit = await service.get(fake_email)
        assert len(default_limit) == 20

        get_all = await service.get(fake_email, limit=30)
        assert len(get_all) == 22

        with_offset = await service.get(fake_email, offset=2, limit=25)
        assert len(with_offset) == 20
        assert with_offset[0].firstname == "Ivan2"


@mark.asyncio
async def test_get_contact_by_id(async_session):
    async for s in async_session:
        service = ContactService(s)
        fake_email = "john.doe@gmail.com"

        contact = await service.create(contact_with_phone_number(), fake_email)
        result = await service.get_by_id(contact.id, fake_email)

        assert type(result) is Contact
        assert result.id == contact.id

        for field, value in contact.__dict__.items():
            assert getattr(result, field) == value


@mark.asyncio
async def test_id_not_found(async_session):
    async for s in async_session:
        service = ContactService(s)
        fakeid = uuid6()
        fake_email = "john.doe@gmail.com"

        with raises(HTTPException):
            await service.get_by_id(fakeid, fake_email)

        with raises(HTTPException):
            await service.delete(fakeid, fake_email)

        with raises(HTTPException):
            await service.update(
                fakeid, fake_email, ContactUpdate(telegram_name="siberian_bear")
            )

        with raises(HTTPException):
            await service.create(company_contact(fakeid), fake_email)


@mark.asyncio
async def test_delete_contact(async_session):
    async for s in async_session:
        service = ContactService(s)
        fake_email = "john.doe@gmail.com"
        contact = await service.create(simple_contact(), fake_email)

        before = await service.get_by_id(contact.id, fake_email)
        assert before == contact

        delete_result = await service.delete(contact.id, fake_email)
        assert delete_result == contact.id

        with raises(HTTPException):
            await service.get_by_id(contact.id, fake_email)


@mark.asyncio
async def test_update_contact(async_session):
    async for s in async_session:
        service = ContactService(s)
        fake_email = "john.doe@gmail.com"
        contact = await service.create(contact_with_phone_number(), fake_email)

        assert contact.firstname == "Ivan"
        assert contact.lastname == "Ivanov"
        assert contact.patronymic is None
        assert contact.phone_number == 79998887766
        assert contact.telegram_name is None
        assert contact.company_id is None

        update1 = await service.update(contact.id, fake_email, ContactUpdate())
        assert update1 == contact
        assert contact.firstname == "Ivan"
        assert contact.lastname == "Ivanov"
        assert contact.patronymic is None
        assert contact.phone_number == 79998887766
        assert contact.telegram_name is None
        assert contact.company_id is None

        update2 = await service.update(
            contact.id, fake_email, ContactUpdate(telegram_name="epicIvan")
        )
        assert update2 == contact
        assert contact.telegram_name == "epicIvan"

        update3 = await service.update(
            contact.id,
            fake_email,
            ContactUpdate(
                firstname="John", patronymic="Ivanovich", phone_number=71112223344
            ),
        )
        assert update3 == contact
        assert contact.firstname == "John"
        assert contact.patronymic == "Ivanovich"
        assert contact.phone_number == 71112223344
