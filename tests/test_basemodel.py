from pytest import mark
from uuid6 import uuid6, UUID
from datetime import datetime
from app.models.base_model import BaseModel


@mark.asyncio
async def test_basemodel():
    model = BaseModel()
    model2 = BaseModel()
    assert type(model.id) is UUID
    assert type(model.created_at) is datetime
    # uuid6 is time ordered
    assert model.id < model2.id
    assert model.created_at < model2.created_at
