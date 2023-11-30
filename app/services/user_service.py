from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserIn
from app.settings import settings


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def register(self, model_in: UserIn) -> User:
        password_hash = self.crypt_context.hash(model_in.password)

        existing = await self.session.get(User, model_in.email)
        if existing is not None:
            raise HTTPException(
                status_code=400, detail="User with given email alreay exists."
            )

        user = User(email=model_in.email, password_hash=password_hash)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def login(self, model_in: UserIn, lifetime=None) -> str:
        user = await self.session.get(User, model_in.email)
        if user is None:
            raise HTTPException(
                status_code=404, detail="User not found with given email"
            )

        if not self.crypt_context.verify(model_in.password, user.password_hash):
            raise HTTPException(
                status_code=401,
                detail="Incorrect credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = self._create_token(user.email, lifetime=lifetime)
        return token

    async def get_logged_in_user(self, token: str) -> User:
        try:
            data = jwt.decode(
                token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
            )
            email = data.get("payload")
        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="Incorrect credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = await self.session.get(User, email)
        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Incorrect credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    def _create_token(self, payload: str, lifetime: Optional[timedelta] = None):
        lifetime = (
            lifetime
            if lifetime is not None
            else timedelta(minutes=settings.JWT_LIFETIME_IN_MINUTES)
        )
        now = datetime.utcnow()
        expires_at = now + lifetime
        data = {"exp": expires_at, "iat": now, "payload": payload}
        return jwt.encode(data, settings.JWT_SECRET, settings.JWT_ALGORITHM)
