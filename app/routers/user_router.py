from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import db
from app.models.user import UserIn
from app.services.user_service import UserService

router = APIRouter()


@router.post("/register", status_code=201)
async def register(user_in: UserIn, session: AsyncSession = Depends(db.get_session)):
    user = await UserService(session).register(user_in)
    return user


@router.post("/login", status_code=200)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(db.get_session),
):
    user_in = UserIn(email=form_data.username, password=form_data.password)
    token = await UserService(session).login(user_in)

    return {"jwt": token}
